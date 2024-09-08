import numpy as np
import ctypes
import struct
import matplotlib.pyplot as plt


pmu_magic = {
    "END": 0x01FF0000,
    "ECG1": 0x01010000,
    "ECG2": 0x01020000,
    "ECG3": 0x01030000,
    "ECG4": 0x01040000,
    "PULS": 0x01050000,
    "RESP": 0x01060000,
    "EXT1": 0x01070000,
    "EXT2": 0x01080000
}

magic_pmu = dict(reversed(item) for item in pmu_magic.items())


class SeqDataHeader(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("packet_size", ctypes.c_uint32),
        ("id", ctypes.c_char * 52),
        ("swapped", ctypes.c_uint32)
    ]


class SeqData():
    def __init__(self, data):
        self.hdr = SeqDataHeader.from_buffer_copy(data)
        self.data = data[ctypes.sizeof(self.hdr):ctypes.sizeof(self.hdr) + self.hdr.packet_size]


class PMUblock():
    def __init__(self, data):
        self.timestamp0, self.timestamp, self.packet_no, self.duration = struct.unpack('IIII', data[:16])
        i = 16
        self.signal = dict()
        self.trigger = dict()
        while i < len(data):
            magic, = struct.unpack('I', data[i:i+4])
            if magic in magic_pmu:
                key = magic_pmu[magic]
            else:
                key = "UNKNOWN"
            i += 4
            if key == 'END':
                break
            period, = struct.unpack('I', data[i:i+4])
            i += 4
            n_pts = int(self.duration/period)
            if magic not in magic_pmu:
                print('unknown magic key', magic, hex(magic))
            else:
                block = np.frombuffer(data[i:i+4*n_pts], dtype=np.uint16).reshape((n_pts, 2)).T
                self.signal[key] = block[0].astype(float) / 4096.
                self.trigger[key] = block[1].astype(bool)
            i += 4*n_pts

    def get_timestamp(self, key):
        n_pts = len(self.signal[key])
        return self.timestamp + np.linspace(0, self.duration/10., n_pts, endpoint=False) / 2.5

    def get_time(self, key):  # in s
        return self.get_timestamp(key) * 2.5e-3


class PMU():
    def __init__(self, mdbs):
        # member variables that will be populated
        self.signal = dict()
        self.trigger = dict()
        self.timestamp = dict()
        self.pmublocks = []  # store blocks

        for mdb in mdbs:
            if not mdb.is_flag_set('SYNCDATA'):
                continue
            seqdata = SeqData(mdb.data)
            if not seqdata.hdr.id.startswith(b'PMU'):
                continue
            is_learning_phase = seqdata.hdr.id.startswith(b'PMULearnPhase')
            block = PMUblock(seqdata.data)
            self.pmublocks.append(block)
            for key in block.signal:
                pmu_key = key
                if is_learning_phase:
                    pmu_key = 'LEARN_' + pmu_key
                if pmu_key not in self.signal:
                    self.signal[pmu_key] = []
                    self.trigger[pmu_key] = []
                    self.timestamp[pmu_key] = []
                self.signal[pmu_key].append(block.signal[key])
                self.trigger[pmu_key].append(block.trigger[key])
                self.timestamp[pmu_key].append(block.get_timestamp(key))
        for pmu_key in self.signal:
            self.signal[pmu_key] = np.concatenate(self.signal[pmu_key])
            self.trigger[pmu_key] = np.concatenate(self.trigger[pmu_key])
            self.timestamp[pmu_key] = np.concatenate(self.timestamp[pmu_key])

    def __str__(self):
        """Convert to string, for str()."""
        return (f"{self.__class__.__module__}.{self.__class__.__qualname__}:\n"
                f"  .signal: dict of pmu waveforms\n"
                f"  .trigger: dict of triggers for each channel\n"
                f"  .timestamp: dict of timestamps for each channel")

    def plot(self, keys=None, show_trigger=True):

        if keys is None:
            keys = list(self.signal.keys())
        elif isinstance(keys, str):
            keys = [keys]

        if show_trigger:
            trig_keys = [key for key in keys if np.any(self.trigger[key])]
            if len(trig_keys) == 0:
                print('No trigger signals found')
                show_trigger = False

        _, axs = plt.subplots(1 + bool(show_trigger), 1, squeeze=False, sharex=True)
        colors = dict()
        for key in keys:
            axs[0, 0].plot(self.timestamp[key], self.signal[key], label=key)
            colors[key] = axs[0, 0].lines[-1].get_color()

        axs[-1, 0].set_xlabel('timestamp [2.5 us ticks from midnight]')
        axs[0, 0].set_ylabel('normalized signal')
        axs[0, 0].legend()

        # add secondary x-axis with time in seconds
        t0 = self.get_time(keys[0])[0]
        secax = axs[0, 0].secondary_xaxis('top', functions=(lambda x: x*2.5e-3 - t0, lambda x: (x + t0) / 2.5e-3))
        secax.set_xlabel('time [s]')

        if show_trigger:
            color = [colors[key] for key in trig_keys]
            event = [self.timestamp[key][self.trigger[key]] for key in trig_keys]
            axs[1, 0].eventplot(event, linelengths=0.8, color=color)
            axs[1, 0].legend(trig_keys)
            axs[1, 0].set_ylabel('trigger signals')

        plt.show()

    def get_time(self, key):  # in s
        return self.timestamp[key] * 2.5e-3

    def get_signal(self, key, timestamp):
        if timestamp < self.timestamp[key][0] or timestamp > self.timestamp[key][-1]:
            return np.nan
        return np.interp(timestamp, self.timestamp[key], self.signal[key])

    def get_trigger(self, key, timestamp):
        if timestamp < self.timestamp[key][0] or timestamp > self.timestamp[key][-1]:
            return np.nan
        # Find next neighbor index
        index = np.searchsorted(self.timestamp[key], timestamp)
        # Ensure the index is within the bounds of the array
        index = np.clip(index, 0, len(timestamp[key]) - 1)
        return self.trigger[key][index]

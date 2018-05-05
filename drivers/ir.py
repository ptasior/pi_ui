import time
import os
import pigpio


GPIO       = 4
GLITCH     = 100
PRE_MS     = 200
POST_MS    = 15
FREQ       = 38.0
VERBOSE    = False
SHORT      = 10
GAP_MS     = 100
TOLERANCE  = 15

POST_US    = POST_MS * 1000
PRE_US     = PRE_MS  * 1000
GAP_S      = GAP_MS  / 1000.0
TOLER_MIN =  (100 - TOLERANCE) / 100.0
TOLER_MAX =  (100 + TOLERANCE) / 100.0

last_tick = 0
in_code = False
code = []
fetching_code = False

KEYS = {
        '0': [9040.0, 4480.0, 601.48, 530.0, 601.48, 530.0, 601.48, 530.0, 601.48, 530.0, 601.48, 530.0, 601.48, 530.0, 601.48, 530.0, 601.48, 530.0, 601.48, 1637.0, 601.48, 1637.0, 601.48, 1637.0, 601.48, 1637.0, 601.48, 1637.0, 601.48, 1637.0, 601.48, 1637.0, 601.48, 1637.0, 601.48, 530.0, 601.48, 1637.0, 601.48, 1637.0, 601.48, 530.0, 601.48, 1637.0, 601.48, 530.0, 601.48, 530.0, 601.48, 530.0, 601.48, 1637.0, 601.48, 530.0, 601.48, 530.0, 601.48, 1637.0, 601.48, 530.0, 601.48, 1637.0, 601.48, 1637.0, 601.48, 1637.0, 601.48],
        '1': [9035.0, 4480.0, 601.36, 529.38, 601.36, 529.38, 601.36, 529.38, 601.36, 529.38, 601.36, 529.38, 601.36, 529.38, 601.36, 529.38, 601.36, 529.38, 601.36, 1637.81, 601.36, 1637.81, 601.36, 1637.81, 601.36, 1637.81, 601.36, 1637.81, 601.36, 1637.81, 601.36, 1637.81, 601.36, 1637.81, 601.36, 529.38, 601.36, 529.38, 601.36, 1637.81, 601.36, 1637.81, 601.36, 529.38, 601.36, 529.38, 601.36, 529.38, 601.36, 529.38, 601.36, 1637.81, 601.36, 1637.81, 601.36, 529.38, 601.36, 529.38, 601.36, 1637.81, 601.36, 1637.81, 601.36, 1637.81, 601.36, 1637.81, 601.36],
        '2': [9040.0, 4480.0, 596.67, 532.19, 596.67, 532.19, 596.67, 532.19, 596.67, 532.19, 596.67, 532.19, 596.67, 532.19, 596.67, 532.19, 596.67, 532.19, 596.67, 1645.0, 596.67, 1645.0, 596.67, 1645.0, 596.67, 1645.0, 596.67, 1645.0, 596.67, 1645.0, 596.67, 1645.0, 596.67, 1645.0, 596.67, 532.19, 596.67, 532.19, 596.67, 532.19, 596.67, 1645.0, 596.67, 1645.0, 596.67, 532.19, 596.67, 532.19, 596.67, 532.19, 596.67, 1645.0, 596.67, 1645.0, 596.67, 1645.0, 596.67, 532.19, 596.67, 532.19, 596.67, 1645.0, 596.67, 1645.0, 596.67, 1645.0, 596.67],
        '3': [9050.0, 4485.0, 597.79, 532.25, 597.79, 532.25, 597.79, 532.25, 597.79, 532.25, 597.79, 532.25, 597.79, 532.25, 597.79, 532.25, 597.79, 532.25, 597.79, 1643.0, 597.79, 1643.0, 597.79, 1643.0, 597.79, 1643.0, 597.79, 1643.0, 597.79, 1643.0, 597.79, 1643.0, 597.79, 1643.0, 597.79, 532.25, 597.79, 1643.0, 597.79, 1643.0, 597.79, 1643.0, 597.79, 1643.0, 597.79, 532.25, 597.79, 1643.0, 597.79, 532.25, 597.79, 1643.0, 597.79, 532.25, 597.79, 532.25, 597.79, 532.25, 597.79, 532.25, 597.79, 1643.0, 597.79, 532.25, 597.79, 1643.0, 597.79],
        '4': [9005.0, 4510.0, 572.24, 559.06, 572.24, 559.06, 572.24, 559.06, 572.24, 559.06, 572.24, 559.06, 572.24, 559.06, 572.24, 559.06, 572.24, 559.06, 572.24, 1665.69, 572.24, 1665.69, 572.24, 1665.69, 572.24, 1665.69, 572.24, 1665.69, 572.24, 1665.69, 572.24, 1665.69, 572.24, 1665.69, 572.24, 559.06, 572.24, 559.06, 572.24, 559.06, 572.24, 1665.69, 572.24, 559.06, 572.24, 559.06, 572.24, 559.06, 572.24, 559.06, 572.24, 1665.69, 572.24, 1665.69, 572.24, 1665.69, 572.24, 559.06, 572.24, 1665.69, 572.24, 1665.69, 572.24, 1665.69, 572.24, 1665.69, 572.24],
        '5': [9035.0, 4485.0, 600.61, 531.56, 600.61, 531.56, 600.61, 531.56, 600.61, 531.56, 600.61, 531.56, 600.61, 531.56, 600.61, 531.56, 600.61, 531.56, 600.61, 1636.88, 600.61, 1636.88, 600.61, 1636.88, 600.61, 1636.88, 600.61, 1636.88, 600.61, 1636.88, 600.61, 1636.88, 600.61, 1636.88, 600.61, 531.56, 600.61, 531.56, 600.61, 1636.88, 600.61, 1636.88, 600.61, 1636.88, 600.61, 531.56, 600.61, 531.56, 600.61, 531.56, 600.61, 1636.88, 600.61, 1636.88, 600.61, 531.56, 600.61, 531.56, 600.61, 531.56, 600.61, 1636.88, 600.61, 1636.88, 600.61, 1636.88, 600.61],
        '6': [9035.0, 4480.0, 600.76, 531.25, 600.76, 531.25, 600.76, 531.25, 600.76, 531.25, 600.76, 531.25, 600.76, 531.25, 600.76, 531.25, 600.76, 531.25, 600.76, 1637.5, 600.76, 1637.5, 600.76, 1637.5, 600.76, 1637.5, 600.76, 1637.5, 600.76, 1637.5, 600.76, 1637.5, 600.76, 1637.5, 600.76, 531.25, 600.76, 1637.5, 600.76, 531.25, 600.76, 1637.5, 600.76, 1637.5, 600.76, 531.25, 600.76, 1637.5, 600.76, 531.25, 600.76, 1637.5, 600.76, 531.25, 600.76, 1637.5, 600.76, 531.25, 600.76, 531.25, 600.76, 1637.5, 600.76, 531.25, 600.76, 1637.5, 600.76],
        '7': [9035.0, 4485.0, 601.03, 531.0, 601.03, 531.0, 601.03, 531.0, 601.03, 531.0, 601.03, 531.0, 601.03, 531.0, 601.03, 531.0, 601.03, 531.0, 601.03, 1636.25, 601.03, 1636.25, 601.03, 1636.25, 601.03, 1636.25, 601.03, 1636.25, 601.03, 1636.25, 601.03, 1636.25, 601.03, 1636.25, 601.03, 531.0, 601.03, 1636.25, 601.03, 531.0, 601.03, 531.0, 601.03, 531.0, 601.03, 531.0, 601.03, 1636.25, 601.03, 531.0, 601.03, 1636.25, 601.03, 531.0, 601.03, 1636.25, 601.03, 1636.25, 601.03, 1636.25, 601.03, 1636.25, 601.03, 531.0, 601.03, 1636.25, 601.03],
        '8': [9035.0, 4480.0, 603.33, 528.13, 603.33, 528.13, 603.33, 528.13, 603.33, 528.13, 603.33, 528.13, 603.33, 528.13, 603.33, 528.13, 603.33, 528.13, 603.33, 1634.69, 603.33, 1634.69, 603.33, 1634.69, 603.33, 1634.69, 603.33, 1634.69, 603.33, 1634.69, 603.33, 1634.69, 603.33, 1634.69, 603.33, 528.13, 603.33, 1634.69, 603.33, 528.13, 603.33, 528.13, 603.33, 1634.69, 603.33, 528.13, 603.33, 1634.69, 603.33, 528.13, 603.33, 1634.69, 603.33, 528.13, 603.33, 1634.69, 603.33, 1634.69, 603.33, 528.13, 603.33, 1634.69, 603.33, 528.13, 603.33, 1634.69, 603.33],
        '9': [9040.0, 4485.0, 602.15, 530.31, 602.15, 530.31, 602.15, 530.31, 602.15, 530.31, 602.15, 530.31, 602.15, 530.31, 602.15, 530.31, 602.15, 530.31, 602.15, 1635.88, 602.15, 1635.88, 602.15, 1635.88, 602.15, 1635.88, 602.15, 1635.88, 602.15, 1635.88, 602.15, 1635.88, 602.15, 1635.88, 602.15, 530.31, 602.15, 1635.88, 602.15, 530.31, 602.15, 1635.88, 602.15, 530.31, 602.15, 530.31, 602.15, 1635.88, 602.15, 530.31, 602.15, 1635.88, 602.15, 530.31, 602.15, 1635.88, 602.15, 530.31, 602.15, 1635.88, 602.15, 1635.88, 602.15, 530.31, 602.15, 1635.88, 602.15],
        'CH-': [9055.0, 4480.0, 601.21, 529.69, 601.21, 529.69, 601.21, 529.69, 601.21, 529.69, 601.21, 529.69, 601.21, 529.69, 601.21, 529.69, 601.21, 529.69, 601.21, 1639.38, 601.21, 1639.38, 601.21, 1639.38, 601.21, 1639.38, 601.21, 1639.38, 601.21, 1639.38, 601.21, 1639.38, 601.21, 1639.38, 601.21, 1639.38, 601.21, 529.69, 601.21, 1639.38, 601.21, 529.69, 601.21, 529.69, 601.21, 529.69, 601.21, 1639.38, 601.21, 529.69, 601.21, 529.69, 601.21, 1639.38, 601.21, 529.69, 601.21, 1639.38, 601.21, 1639.38, 601.21, 1639.38, 601.21, 529.69, 601.21, 1639.38, 601.21],
        'CH+': [9049.0, 4481.0, 603.48, 528.13, 603.48, 528.13, 603.48, 528.13, 603.48, 528.13, 603.48, 528.13, 603.48, 528.13, 603.48, 528.13, 603.48, 528.13, 603.48, 1635.63, 603.48, 1635.63, 603.48, 1635.63, 603.48, 1635.63, 603.48, 1635.63, 603.48, 1635.63, 603.48, 1635.63, 603.48, 1635.63, 603.48, 1635.63, 603.48, 1635.63, 603.48, 1635.63, 603.48, 528.13, 603.48, 528.13, 603.48, 528.13, 603.48, 1635.63, 603.48, 528.13, 603.48, 528.13, 603.48, 528.13, 603.48, 528.13, 603.48, 1635.63, 603.48, 1635.63, 603.48, 1635.63, 603.48, 528.13, 603.48, 1635.63, 603.48],
        'PREV': [9050.0, 4481.0, 598.39, 534.69, 598.39, 534.69, 598.39, 534.69, 598.39, 534.69, 598.39, 534.69, 598.39, 534.69, 598.39, 534.69, 598.39, 534.69, 598.39, 1639.25, 598.39, 1639.25, 598.39, 1639.25, 598.39, 1639.25, 598.39, 1639.25, 598.39, 1639.25, 598.39, 1639.25, 598.39, 1639.25, 598.39, 534.69, 598.39, 534.69, 598.39, 1639.25, 598.39, 534.69, 598.39, 534.69, 598.39, 534.69, 598.39, 1639.25, 598.39, 534.69, 598.39, 1639.25, 598.39, 1639.25, 598.39, 534.69, 598.39, 1639.25, 598.39, 1639.25, 598.39, 1639.25, 598.39, 534.69, 598.39, 1639.25, 598.39],
        'NEXT': [9050.0, 4480.0, 604.09, 527.81, 604.09, 527.81, 604.09, 527.81, 604.09, 527.81, 604.09, 527.81, 604.09, 527.81, 604.09, 527.81, 604.09, 527.81, 604.09, 1635.0, 604.09, 1635.0, 604.09, 1635.0, 604.09, 1635.0, 604.09, 1635.0, 604.09, 1635.0, 604.09, 1635.0, 604.09, 1635.0, 604.09, 527.81, 604.09, 527.81, 604.09, 527.81, 604.09, 527.81, 604.09, 527.81, 604.09, 527.81, 604.09, 1635.0, 604.09, 527.81, 604.09, 1635.0, 604.09, 1635.0, 604.09, 1635.0, 604.09, 1635.0, 604.09, 1635.0, 604.09, 1635.0, 604.09, 527.81, 604.09, 1635.0, 604.09],
        'PLAY': [9065.0, 4480.0, 590.15, 537.81, 590.15, 537.81, 590.15, 537.81, 590.15, 537.81, 590.15, 537.81, 590.15, 537.81, 590.15, 537.81, 590.15, 537.81, 590.15, 1652.81, 590.15, 1652.81, 590.15, 1652.81, 590.15, 1652.81, 590.15, 1652.81, 590.15, 1652.81, 590.15, 1652.81, 590.15, 1652.81, 590.15, 1652.81, 590.15, 1652.81, 590.15, 537.81, 590.15, 537.81, 590.15, 537.81, 590.15, 537.81, 590.15, 1652.81, 590.15, 537.81, 590.15, 537.81, 590.15, 537.81, 590.15, 1652.81, 590.15, 1652.81, 590.15, 1652.81, 590.15, 1652.81, 590.15, 537.81, 590.15, 1652.81, 590.15],
        '-': [9050.0, 4480.0, 604.48, 528.0, 604.48, 528.0, 604.48, 528.0, 604.48, 528.0, 604.48, 528.0, 604.48, 528.0, 604.48, 528.0, 604.48, 528.0, 604.48, 1634.0, 604.48, 1634.0, 604.48, 1634.0, 604.48, 1634.0, 604.48, 1634.0, 604.48, 1634.0, 604.48, 1634.0, 604.48, 1634.0, 604.48, 1634.0, 604.48, 1634.0, 604.48, 1634.0, 604.48, 528.0, 604.48, 528.0, 604.48, 528.0, 604.48, 528.0, 604.48, 528.0, 604.48, 528.0, 604.48, 528.0, 604.48, 528.0, 604.48, 1634.0, 604.48, 1634.0, 604.48, 1634.0, 604.48, 1634.0, 604.48, 1634.0, 604.48],
        '+': [9060.0, 4480.0, 595.61, 535.94, 595.61, 535.94, 595.61, 535.94, 595.61, 535.94, 595.61, 535.94, 595.61, 535.94, 595.61, 535.94, 595.61, 535.94, 595.61, 1643.75, 595.61, 1643.75, 595.61, 1643.75, 595.61, 1643.75, 595.61, 1643.75, 595.61, 1643.75, 595.61, 1643.75, 595.61, 1643.75, 595.61, 1643.75, 595.61, 535.94, 595.61, 1643.75, 595.61, 535.94, 595.61, 1643.75, 595.61, 535.94, 595.61, 535.94, 595.61, 535.94, 595.61, 535.94, 595.61, 1643.75, 595.61, 535.94, 595.61, 1643.75, 595.61, 535.94, 595.61, 1643.75, 595.61, 1643.75, 595.61, 1643.75, 595.61],
        'EQ': [9030.0, 4510.0, 580.91, 549.69, 580.91, 549.69, 580.91, 549.69, 580.91, 549.69, 580.91, 549.69, 580.91, 549.69, 580.91, 549.69, 580.91, 549.69, 580.91, 1660.31, 580.91, 1660.31, 580.91, 1660.31, 580.91, 1660.31, 580.91, 1660.31, 580.91, 1660.31, 580.91, 1660.31, 580.91, 1660.31, 580.91, 1660.31, 580.91, 549.69, 580.91, 549.69, 580.91, 1660.31, 580.91, 549.69, 580.91, 549.69, 580.91, 549.69, 580.91, 549.69, 580.91, 549.69, 580.91, 1660.31, 580.91, 1660.31, 580.91, 549.69, 580.91, 1660.31, 580.91, 1660.31, 580.91, 1660.31, 580.91, 1660.31, 580.91]
    }


class IR(object):
    def __init__(self):
        global pi
        pi = pigpio.pi() # Connect to Pi.

        if not pi.connected:
           raise Exception("Can not connect to pigpiod. Is it started?")



    def cleanup(self):
        global pi
        pi.stop() # Disconnect from Pi.



    @staticmethod 
    def carrier(gpio, frequency, micros):
        """
        Generate carrier square wave.
        """
        wf = []
        cycle = 1000.0 / frequency
        cycles = int(round(micros/cycle))
        on = int(round(cycle / 2.0))
        sofar = 0
        for c in range(cycles):
            target = int(round((c+1)*cycle))
            sofar += on
            off = target - sofar
            sofar += off
            wf.append(pigpio.pulse(1<<gpio, 0, on))
            wf.append(pigpio.pulse(0, 1<<gpio, off))
        return wf



    @staticmethod 
    def normalise(c):
        """
        Typically a code will be made up of two or three distinct
        marks (carrier) and spaces (no carrier) of different lengths.

        Because of transmission and reception errors those pulses
        which should all be x micros long will have a variance around x.

        This function identifies the distinct pulses and takes the
        average of the lengths making up each distinct pulse.  Marks
        and spaces are processed separately.

        This makes the eventual generation of waves much more efficient.

        Input

           M     S    M    S    M    S    M     S    M     S    M
        9000 4500 600 540 620 560 590 1660 620 1690 615

        Distinct marks

        9000                     average 9000
        600 620 590 620 615 average  609

        Distinct spaces

        4500                     average 4500
        540 560                 average  550
        1660 1690              average 1675

        Output

           M     S    M    S    M    S    M     S    M     S    M
        9000 4500 609 550 609 550 609 1675 609 1675 609
        """
        if VERBOSE:
            print("before normalise", c)
        entries = len(c)
        p = [0]*entries # Set all entries not processed.
        for i in range(entries):
            if not p[i]: # Not processed?
                v = c[i]
                tot = v
                similar = 1.0

                # Find all pulses with similar lengths to the start pulse.
                for j in range(i+2, entries, 2):
                    if not p[j]: # Unprocessed.
                        if (c[j]*TOLER_MIN) < v < (c[j]*TOLER_MAX): # Similar.
                            tot = tot + c[j]
                            similar += 1.0

                # Calculate the average pulse length.
                newv = round(tot / similar, 2)
                c[i] = newv

                # Set all similar pulses to the average value.
                for j in range(i+2, entries, 2):
                    if not p[j]: # Unprocessed.
                        if (c[j]*TOLER_MIN) < v < (c[j]*TOLER_MAX): # Similar.
                            c[j] = newv
                            p[j] = 1

        if VERBOSE:
            print("after normalise", c)



    @staticmethod
    def compare(p1, p2):
        """
        Check that both recodings correspond in pulse length to within
        TOLERANCE%.  If they do average the two recordings pulse lengths.

        Input

               M     S    M    S    M    S    M     S    M     S    M
        1: 9000 4500 600 560 600 560 600 1700 600 1700 600
        2: 9020 4570 590 550 590 550 590 1640 590 1640 590

        Output

        A: 9010 4535 595 555 595 555 595 1670 595 1670 595
        """
        if VERBOSE:
            print("cmp: len1: "+str(len(p1))+' len2: '+str(len(p2)))

        if len(p1) != len(p2):
            return False

        for i in range(len(p1)):
            v = p1[i] / p2[i]
            if (v < TOLER_MIN) or (v > TOLER_MAX):
                return False

        for i in range(len(p1)):
            p1[i] = int(round((p1[i]+p2[i])/2.0))

        if VERBOSE:
            print("after compare", p1)

        return True



    @staticmethod
    def tidy_mark_space(records, base):
        ms = {}

        # Find all the unique marks (base=0) or spaces (base=1)
        # and count the number of times they appear,

        for rec in records:
            rl = len(records[rec])
            for i in range(base, rl, 2):
                if records[rec][i] in ms:
                    ms[records[rec][i]] += 1
                else:
                    ms[records[rec][i]] = 1

        if VERBOSE:
            print("t_m_s A", ms)

        v = None

        for plen in sorted(ms):

            # Now go through in order, shortest first, and collapse
            # pulses which are the same within a tolerance to the
            # same value.  The value is the weighted average of the
            # occurences.
            #
            # E.g. 500x20 550x30 600x30  1000x10 1100x10  1700x5 1750x5
            #
            # becomes 556(x80) 1050(x20) 1725(x10)
            #
            if v == None:
                e = [plen]
                v = plen
                tot = plen * ms[plen]
                similar = ms[plen]

            elif plen < (v*TOLER_MAX):
                e.append(plen)
                tot += (plen * ms[plen])
                similar += ms[plen]

            else:
                v = int(round(tot/float(similar)))
                # set all previous to v
                for i in e:
                    ms[i] = v
                e = [plen]
                v = plen
                tot = plen * ms[plen]
                similar = ms[plen]

        v = int(round(tot/float(similar)))
        # set all previous to v
        for i in e:
            ms[i] = v

        if VERBOSE:
            print("t_m_s B", ms)

        for rec in records:
            rl = len(records[rec])
            for i in range(base, rl, 2):
                records[rec][i] = ms[records[rec][i]]



    @staticmethod
    def tidy(records):
        IR.tidy_mark_space(records, 0) # Marks.
        IR.tidy_mark_space(records, 1) # Spaces.



    @staticmethod 
    def end_of_code():
        global code, fetching_code

        if len(code) > SHORT:
            IR.normalise(code)
            fetching_code = False
        else:
            code = []
            print("Short code, probably a repeat, try again")


    @staticmethod 
    def cbf(gpio, level, tick):
        global last_tick, in_code, code, fetching_code, pi

        if level == pigpio.TIMEOUT:
            pi.set_watchdog(GPIO, 0) # Cancel watchdog.
            if in_code:
                in_code = False
                IR.end_of_code()
            return

        edge = pigpio.tickDiff(last_tick, tick)
        last_tick = tick

        if fetching_code:
            if (edge > PRE_US) and (not in_code): # Start of a code.
                in_code = True
                pi.set_watchdog(GPIO, POST_MS) # Start watchdog.
            elif (edge > POST_US) and in_code: # End of a code.
                in_code = False
                pi.set_watchdog(GPIO, 0) # Cancel watchdog.
                IR.end_of_code()
            elif in_code:
                code.append(edge)



    def translate(self, code):
        for k,v in KEYS.items():
            if(IR.compare(v, code)):
                return k
        return 'UNKNOWN'



    def listenAndPrint(self):
        global code, fetching_code, pi

        pi.set_mode(GPIO, pigpio.INPUT) # IR RX connected to this GPIO.
        pi.set_glitch_filter(GPIO, GLITCH) # Ignore glitches.
        cb = pi.callback(GPIO, pigpio.EITHER_EDGE, IR.cbf)

        print("Listening")

        while True:
            code = []
            fetching_code = True
            while fetching_code:
                time.sleep(0.1)
            print("Received: \n"+str(code))
            time.sleep(0.5)

        # pi.set_glitch_filter(GPIO, 0) # Cancel glitch filter.
        # pi.set_watchdog(GPIO, 0) # Cancel watchdog.
        #
        # self.tidy(records)



    def listen(self, handler):
        global code, fetching_code, pi

        pi.set_mode(GPIO, pigpio.INPUT) # IR RX connected to this GPIO.
        pi.set_glitch_filter(GPIO, GLITCH) # Ignore glitches.
        cb = pi.callback(GPIO, pigpio.EITHER_EDGE, IR.cbf)

        if VERBOSE:
            print("Listening")

        while True:
            code = []
            fetching_code = True
            while fetching_code:
                time.sleep(0.1)
            if VERBOSE:
                print("Received: \n"+str(code))

            key = self.translate(code)
            handler(key)

            time.sleep(0.5)

        # pi.set_glitch_filter(GPIO, 0) # Cancel glitch filter.
        # pi.set_watchdog(GPIO, 0) # Cancel watchdog.
        #
        # self.tidy(records)


    # def playback(self):
    #     pass
        # global code, fetching_code, pi
        # try:
        #     f = open(FILE, "r")
        # except:
        #     print("Can't open: {}".format(FILE))
        #     exit(0)
        #
        # records = json.load(f)
        #
        # f.close()
        #
        # pi.set_mode(GPIO, pigpio.OUTPUT) # IR TX connected to this GPIO.
        #
        # pi.wave_add_new()
        #
        # emit_time = time.time()
        #
        # if VERBOSE:
        #     print("Playing")
        #
        # for arg in args.id:
        #     if arg in records:
        #
        #         code = records[arg]
        #
        #         # Create wave
        #
        #         marks_wid = {}
        #         spaces_wid = {}
        #
        #         wave = [0]*len(code)
        #
        #         for i in range(0, len(code)):
        #             ci = code[i]
        #             if i & 1: # Space
        #                 if ci not in spaces_wid:
        #                     pi.wave_add_generic([pigpio.pulse(0, 0, ci)])
        #                     spaces_wid[ci] = pi.wave_create()
        #                 wave[i] = spaces_wid[ci]
        #             else: # Mark
        #                 if ci not in marks_wid:
        #                     wf = self.carrier(GPIO, FREQ, ci)
        #                     pi.wave_add_generic(wf)
        #                     marks_wid[ci] = pi.wave_create()
        #                 wave[i] = marks_wid[ci]
        #
        #         delay = emit_time - time.time()
        #
        #         if delay > 0.0:
        #             time.sleep(delay)
        #
        #         pi.wave_chain(wave)
        #
        #         if VERBOSE:
        #             print("key " + arg)
        #
        #         while pi.wave_tx_busy():
        #             time.sleep(0.002)
        #
        #         emit_time = time.time() + GAP_S
        #
        #         for i in marks_wid:
        #             pi.wave_delete(marks_wid[i])
        #
        #         marks_wid = {}
        #
        #         for i in spaces_wid:
        #             pi.wave_delete(spaces_wid[i])
        #
        #         spaces_wid = {}
        #     else:
        #         print("Id {} not found".format(arg))


if __name__ == '__main__':
    def p(x):
        print('RCD: '+x)

    ir = IR()
    # ir.listenAndPrint()
    ir.listen(p)
    ir.cleanup()


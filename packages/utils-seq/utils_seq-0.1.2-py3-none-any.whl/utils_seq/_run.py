import Bio.Seq as _Seq
import gravy as _gravy
from seqpad import seqpad as pad


def cut(seq: "nucleotide sequence", start=None, stop=None):
    if start is None:
        start = 0
    if stop is None:
        stop = len(seq)
    a = min(0, start)
    b = max(0, start)
    c = min(len(seq), stop)
    d = max(len(seq), stop)
    if b > c:
        return IndexError
    return ("N" * (b - a)) + seq[b:c] + ("N" * (d - c))


def tr(seq: "nucleotide sequence"):
    seq = _Seq.Seq(pad(seq))
    return str(seq.translate())


def gravy(seq: "nucleotide sequence"):
    return _gravy.calculate(tr(seq))

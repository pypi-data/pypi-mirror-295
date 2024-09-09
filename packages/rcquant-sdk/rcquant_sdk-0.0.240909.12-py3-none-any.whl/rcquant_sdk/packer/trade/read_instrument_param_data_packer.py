from ...interface import IPacker


class ReadInstrumentParamDataPacker(IPacker):
    def __init__(self, obj) -> None:
        super().__init__(obj)

    def obj_to_tuple(self):
        return [list(self._obj.ExchangeID), list(self._obj.InstrumentID),
                list(self._obj.UniCode), list(self._obj.DataList),
                str(self._obj.BasePath)]

    def tuple_to_obj(self, t):
        if len(t) >= 5:
            self._obj.ExchangeID = t[0]
            self._obj.InstrumentID = t[1]
            self._obj.UniCode = t[2]
            self._obj.DataList = t[3]
            self._obj.BasePath = t[4]

            return True
        return False

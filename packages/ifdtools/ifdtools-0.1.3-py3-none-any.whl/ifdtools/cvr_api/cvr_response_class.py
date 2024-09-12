from dataclasses import dataclass

@dataclass
class CVRResponse:
    """Klasse som håndteret et respons fra CVR
    
    OBS! Skal skrives om - alt for megen redundans omkring hvilke parametre som returneres.
    NB! Det antages at der tages udgangspunkt i det fulde response - altså uden selektering i output via query."""
    response: dict
    
    def __post_init__(self):
        if self.__invalid_input():
            raise TypeError("response er ikke en dict med det forventede format")
        self.__resp_type = self.__extract_resp_type()
        self.__meta_data = self.__extract_meta_data()
    
    def __invalid_input(self) -> bool:
        """Udestår"""
        return False
    
    def __extract_resp_type(self) -> str:
        """Udleder hvorvidt reponse er på cvr- eller p-nummer."""
        return "cvr" if self.response["_source"].get("Vrvirksomhed") else "pnr"
        
    def __extract_meta_data(self) -> dict:
        if self.__resp_type == "cvr":
            return self.response["_source"]["Vrvirksomhed"]["virksomhedMetadata"]
        else:
            return self.response["_source"]["VrproduktionsEnhed"]["produktionsEnhedMetadata"]

    def get_data(self, all: bool = False, unit: str = "mdr") -> dict | list[dict]:
        if not all:
            return self.__get_latest()
        return self.__get_all(unit)
        
    def __get_latest(self) -> dict:
        results = self.__standard_info
        distinct_info = {
            "ant_ansatte": self.ant_ansatte,
            "ant_aarsvaerk": self.ant_aarsvaerk,
            "ant_ansatte_yyyymm": self.ant_ansatte_yyyymm,
            }
        full_results = results | distinct_info
        return full_results

    def __get_all(self, unit: str) -> list[dict]:
        results = []
        hist_results_ant_ans = self.__get_hist_data()
        if hist_results_ant_ans:
            for k in hist_results_ant_ans:
                temp_res = self.__standard_info
                distinct_info = {
                    "ant_ansatte": k["antalAnsatte"],
                    "ant_aarsvaerk": k["antalAarsvaerk"],
                    "ts_aar": k["aar"],
                    "ts_mdr": k["maaned"],
                }
                results.append(temp_res | distinct_info)
        else:
            temp_res = self.__standard_info
            results.append(temp_res)

        if unit == "mdr":
            return results
        reduced_result = self.__reduce_hist_results(results, unit)
        return reduced_result
    
    def __reduce_hist_results(self, complete_results: list[dict], unit: str) -> list[dict]:
        # Sikrer sortering
        ensure_sorted = sorted(complete_results, key=lambda k: (k["ts_aar"], k["ts_mdr"]), reverse=True)
        finale_res = []
        handled = []
        for k in ensure_sorted:
            if k["ts_aar"] not in handled:
                handled.append(k["ts_aar"])
                finale_res.append(k)
        return finale_res
    
    def __get_hist_data(self) -> list[dict]:
        try:
            hist_data = self.response["_source"]["Vrvirksomhed"]["maanedsbeskaeftigelse"] + self.response["_source"]["Vrvirksomhed"]["erstMaanedsbeskaeftigelse"]
        except KeyError:
            hist_data = self.response["_source"]["Vrvirksomhed"]["maanedsbeskaeftigelse"]
        return hist_data
    
    @property
    def __standard_info(self) -> dict:
        """
        Reference til de standard informationer fra CVR som bruges på tværs af forskellige funktioner.
        Lavet for at gøre det lettere at tilføje nye informationer, idet de dermed kun skal angives ét sted.
        """
        std_info = {
            "cvr": self.cvr,
            "cvr_str": str(self.cvr),
            "name": self.name,
            "kommunekode": self.kommunekode,
            "stiftelsesdato": self.stiftelses_dato,
            "h_branche": self.hbranche,
            "virkform_kode": self.virkform,
            "virkform": self.virkform_str,
            "status": self.status,            
        }
        return std_info
        
    @property
    def cvr(self) -> int:
        if self.__resp_type == "cvr":
            return self.response["_source"]["Vrvirksomhed"]["cvrNummer"]
        else:
            try:
                return self.response["_source"]["VrproduktionsEnhed"]["virksomhedsrelation"][0]["cvrNummer"]
            except IndexError:
                return None
    
    @property
    def hbranche(self) -> int:
        return self.__meta_data["nyesteHovedbranche"]["branchekode"] 

    @property
    def name(self) -> str:
        try: 
            return self.__meta_data["nyesteNavn"]["navn"]
        except TypeError:
            return "NB! nyesteNavn er ikke registreret på virksomheden"
        
    @property
    def status(self) -> str:
        return self.__meta_data["sammensatStatus"]
    
    @property
    def virkform_str(self) -> str:
        return self.__meta_data["nyesteVirksomhedsform"]["langBeskrivelse"]

    @property
    def virkform(self) -> int:
        return self.__meta_data["nyesteVirksomhedsform"]["virksomhedsformkode"]
        
    @property
    def ant_ansatte(self) -> int:
        try: 
            temp = self.__meta_data["nyesteErstMaanedsbeskaeftigelse"]
        except KeyError:
            return None
        try: 
            return self.__meta_data["nyesteErstMaanedsbeskaeftigelse"]["antalAnsatte"]
        except TypeError:
            return None

    @property
    def ant_aarsvaerk(self) -> int:
        try: 
            temp = self.__meta_data["nyesteErstMaanedsbeskaeftigelse"]
        except KeyError:
            return None        
        try: 
            return self.__meta_data["nyesteErstMaanedsbeskaeftigelse"]["antalAarsvaerk"]
        except TypeError:
            return None

    @property
    def ant_ansatte_yyyymm(self) -> int:
        try: 
            temp = self.__meta_data["nyesteErstMaanedsbeskaeftigelse"]
        except KeyError:
            return None        
        try:
            aar = self.__meta_data["nyesteErstMaanedsbeskaeftigelse"]["aar"]
            mdr = self.__meta_data["nyesteErstMaanedsbeskaeftigelse"]["maaned"]
            result = f"{(aar*100)+mdr:02d}"
            return int(result)
        except TypeError:
            return None
        
    @property
    def kommunekode(self) -> int:
        try:
            return int(self.__meta_data["nyesteBeliggenhedsadresse"]["kommune"]["kommuneKode"])
        except KeyError:
            return None

    @property
    def stiftelses_dato(self) -> str:
        try:
            return self.__meta_data["stiftelsesDato"]
        except KeyError:
            return None

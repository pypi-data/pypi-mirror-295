# -*- coding: utf-8 -*-

"""
The commands of seavoice-sdk
"""
import asyncio
import base64
from abc import ABC
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, ClassVar, List, Optional


class SpeechCommand(str, Enum):
    STOP = "stop"
    AUTHENTICATION = "authentication"
    AUDIO_DATA = "audio_data"
    SYNTHESIS = "synthesis"


class Voice(str, Enum):
    TONGTONG = "Tongtong"
    VIVIAN = "Vivian"
    MIKE = "Mike"
    MOXIE = "Moxie"
    LISSA = "Lissa"
    TOM = "Tom"
    ROBERT = "Robert"
    DAVID = "David"
    ANNE = "Anne"
    REESE = "Reese"


class LanguageCode(str, Enum):
    AUTO = "auto"
    AF_AF = "af-AF"  # Afrikaans
    SQ_SQ = "sq-SQ"  # Albanian
    AR_DZ = "ar-DZ"  # Arabic (Algeria)
    AR_BH = "ar-BH"  # Arabic (Bahrain)
    AR_EG = "ar-EG"  # Arabic (Egypt)
    AR_IQ = "ar-IQ"  # Arabic (Iraq)
    AR_JO = "ar-JO"  # Arabic (Jordan)
    AR_KW = "ar-KW"  # Arabic (Kuwait)
    AR_LB = "ar-LB"  # Arabic (Lebanon)
    AR_LY = "ar-LY"  # Arabic (Libya)
    AR_MA = "ar-MA"  # Arabic (Morocco)
    AR_OM = "ar-OM"  # Arabic (Oman)
    AR_QA = "ar-QA"  # Arabic (Qatar)
    AR_SA = "ar-SA"  # Arabic (Saudi Arabia)
    AR_SY = "ar-SY"  # Arabic (Syria)
    AR_TN = "ar-TN"  # Arabic (Tunisia)
    AR_AE = "ar-AE"  # Arabic (U.A.E.)
    AR_YE = "ar-YE"  # Arabic (Yemen)
    EU_EU = "eu-EU"  # Basque
    BE_BE = "be-BE"  # Belarusian
    BG_BG = "bg-BG"  # Bulgarian
    CA_CA = "ca-CA"  # Catalan
    ZH_HK = "zh-HK"  # Chinese (Hong Kong)
    ZH_CN = "zh-CN"  # Chinese (PRC)
    ZH_SG = "zh-SG"  # Chinese (Singapore)
    ZH_TW = "zh-TW"  # Chinese (Taiwan)
    HR_HR = "hr-HR"  # Croatian
    CS_CS = "cs-CS"  # Czech
    DA_DA = "da-DA"  # Danish
    NL_BE = "nl-BE"  # Dutch (Belgium)
    NL_NL = "nl-NL"  # Dutch (Standard)
    EN_EN = "en-EN"  # English
    EN_AU = "en-AU"  # English (Australia)
    EN_BZ = "en-BZ"  # English (Belize)
    EN_CA = "en-CA"  # English (Canada)
    EN_IE = "en-IE"  # English (Ireland)
    EN_JM = "en-JM"  # English (Jamaica)
    EN_NZ = "en-NZ"  # English (New Zealand)
    EN_ZA = "en-ZA"  # English (South Africa)
    EN_TT = "en-TT"  # English (Trinidad)
    EN_GB = "en-GB"  # English (United Kingdom)
    EN_US = "en-US"  # English (United States)
    ET_ET = "et-ET"  # Estonian
    FO_FO = "fo-FO"  # Faeroese
    FA_FA = "fa-FA"  # Farsi
    FI_FI = "fi-FI"  # Finnish
    FR_BE = "fr-BE"  # French (Belgium)
    FR_CA = "fr-CA"  # French (Canada)
    FR_LU = "fr-LU"  # French (Luxembourg)
    FR_FR = "fr-FR"  # French (Standard)
    FR_CH = "fr-CH"  # French (Switzerland)
    GD_GD = "gd-GD"  # Gaelic (Scotland)
    DE_AT = "de-AT"  # German (Austria)
    DE_LI = "de-LI"  # German (Liechtenstein)
    DE_LU = "de-LU"  # German (Luxembourg)
    DE_DE = "de-DE"  # German (Standard)
    DE_CH = "de-CH"  # German (Switzerland)
    EL_EL = "el-EL"  # Greek
    HE_HE = "he-HE"  # Hebrew
    HI_HI = "hi-HI"  # Hindi
    HU_HU = "hu-HU"  # Hungarian
    IS_IS = "is-IS"  # Icelandic
    ID_ID = "id-ID"  # Indonesian
    GA_GA = "ga-GA"  # Irish
    IT_IT = "it-IT"  # Italian (Standard)
    IT_CH = "it-CH"  # Italian (Switzerland)
    JA_JP = "ja-JP"  # Japanese
    KO_KR = "ko-KR"  # Korean
    KU_KU = "ku-KU"  # Kurdish
    LV_LV = "lv-LV"  # Latvian
    LT_LT = "lt-LT"  # Lithuanian
    MK_MK = "mk-MK"  # Macedonian (FYROM)
    ML_ML = "ml-ML"  # Malayalam
    MS_MS = "ms-MS"  # Malaysian
    MT_MT = "mt-MT"  # Maltese
    NO_NO = "no-NO"  # Norwegian
    NB_NB = "nb-NB"  # Norwegian (Bokmål)
    NN_NN = "nn-NN"  # Norwegian (Nynorsk)
    PL_PL = "pl-PL"  # Polish
    PT_BR = "pt-BR"  # Portuguese (Brazil)
    PT_PT = "pt-PT"  # Portuguese (Portugal)
    PA_PA = "pa-PA"  # Punjabi
    RM_RM = "rm-RM"  # Rhaeto-ROmanic
    RO_RO = "ro-RO"  # Romanian
    RO_MD = "ro-MD"  # Romanian (Republic of Moldova)
    RU_RU = "ru-RU"  # Russian
    RU_MD = "ru-MD"  # Russian (Republic of Moldova)
    SR_SR = "sr-SR"  # Serbian
    SK_SK = "sk-SK"  # Slovak
    SL_SL = "sl-SL"  # Slovenian
    SB_SB = "sb-SB"  # Sorbian
    ES_AR = "es-AR"  # Spanish (Argentina)
    ES_BO = "es-BO"  # Spanish (Bolivia)
    ES_CL = "es-CL"  # Spanish (Chile)
    ES_CO = "es-CO"  # Spanish (Colombia)
    ES_CR = "es-CR"  # Spanish (Costa Rica)
    ES_DO = "es-DO"  # Spanish (Dominican Republic)
    ES_EC = "es-EC"  # Spanish (Ecuador)
    ES_SV = "es-SV"  # Spanish (El Salvador)
    ES_GT = "es-GT"  # Spanish (Guatemala)
    ES_HN = "es-HN"  # Spanish (Honduras)
    ES_MX = "es-MX"  # Spanish (Mexico)
    ES_NI = "es-NI"  # Spanish (Nicaragua)
    ES_PA = "es-PA"  # Spanish (Panama)
    ES_PY = "es-PY"  # Spanish (Paraguay)
    ES_PE = "es-PE"  # Spanish (Peru)
    ES_PR = "es-PR"  # Spanish (Puerto Rico)
    ES_ES = "es-ES"  # Spanish (Spain)
    ES_UY = "es-UY"  # Spanish (Uruguay)
    ES_VE = "es-VE"  # Spanish (Venezuela)
    SV_SV = "sv-SV"  # Swedish
    SV_FI = "sv-FI"  # Swedish (Finland)
    TH_TH = "th-TH"  # Thai
    TS_TS = "ts-TS"  # Tsonga
    TN_TN = "tn-TN"  # Tswana
    TR_TR = "tr-TR"  # Turkish
    UA_UA = "ua-UA"  # Ukrainian
    UR_UR = "ur-UR"  # Urdu
    VE_VE = "ve-VE"  # Venda
    VI_VI = "vi-VI"  # Vietnamese
    CY_CY = "cy-CY"  # Welsh
    XH_XH = "xh-XH"  # Xhosa
    JI_JI = "ji-JI"  # Yiddish
    ZU_ZU = "zu-ZU"  # Zulu


VOICE_LANGUAGES_MAPPING = {
    Voice.TONGTONG: [LanguageCode.ZH_TW],
    Voice.VIVIAN: [LanguageCode.ZH_TW],
    Voice.MIKE: [LanguageCode.EN_US],
    Voice.MOXIE: [LanguageCode.EN_US],
    Voice.LISSA: [LanguageCode.EN_US],
    Voice.TOM: [LanguageCode.EN_US],
    Voice.ROBERT: [LanguageCode.EN_US],
    Voice.DAVID: [LanguageCode.EN_GB],
    Voice.ANNE: [LanguageCode.EN_US],
    Voice.REESE: [LanguageCode.EN_US],
}


@dataclass
class AbstractDataclass(ABC):
    def __new__(cls, *args, **kwargs):
        if cls == AbstractDataclass or cls.__bases__[0] == AbstractDataclass:
            raise TypeError("Cannot instantiate abstract class.")
        return super().__new__(cls)


@dataclass
class BaseCommand(AbstractDataclass):
    command: ClassVar[SpeechCommand]
    payload: Any

    def to_dict(self) -> dict:
        return {"command": self.command, "payload": asdict(self.payload)}


@dataclass
class StopCommand(BaseCommand):
    command: ClassVar[SpeechCommand] = SpeechCommand.STOP
    payload: Any = None

    def to_dict(self) -> dict:
        return {"command": self.command}


@dataclass
class BaseAuthenticationPayload(AbstractDataclass):
    token: str
    settings: Any


@dataclass
class SpeechRecognitionSetting:
    language: str
    sample_rate: int
    itn: bool
    punctuation: bool
    contexts: dict
    context_score: float
    stt_server_id: Optional[str]
    # current supports: ["wav_pcm", "flac", "aac", "opus", "mp3", "ogg", "m4a"]
    audio_format: str


@dataclass
class SpeechRecognitionAuthenticationPayload(BaseAuthenticationPayload):
    token: str
    settings: SpeechRecognitionSetting


@dataclass
class SpeechRecognitionAuthenticationCommand(BaseCommand):
    command: ClassVar[SpeechCommand] = SpeechCommand.AUTHENTICATION
    payload: SpeechRecognitionAuthenticationPayload


@dataclass
class SpeechSynthesisSetting:
    language: LanguageCode
    voice: Voice
    tts_server_id: Optional[str]


@dataclass
class SpeechSynthesisAuthenticationPayload(BaseAuthenticationPayload):
    token: str
    settings: SpeechSynthesisSetting


@dataclass
class SpeechSynthesisAuthenticationCommand(BaseCommand):
    command: ClassVar[SpeechCommand] = SpeechCommand.AUTHENTICATION
    payload: SpeechSynthesisAuthenticationPayload


@dataclass
class AudioDataCommand(BaseCommand):
    command: ClassVar[SpeechCommand] = SpeechCommand.AUDIO_DATA
    payload: bytes

    def to_dict(self) -> dict:
        return {
            "command": self.command,
            "payload": base64.b64encode(self.payload).decode(),
        }


@dataclass
class MultiCommands:
    commands: List[BaseCommand]
    done: asyncio.Event


@dataclass
class SynthesisSettings:
    pitch: float
    speed: float
    volume: float
    rules: str
    sample_rate: int


@dataclass
class SynthesisData:
    text: str
    ssml: bool


@dataclass
class SynthesisPayload:
    settings: SynthesisSettings
    data: SynthesisData


@dataclass
class SynthesisCommand(BaseCommand):
    command: ClassVar[SpeechCommand] = SpeechCommand.SYNTHESIS
    payload: SynthesisPayload

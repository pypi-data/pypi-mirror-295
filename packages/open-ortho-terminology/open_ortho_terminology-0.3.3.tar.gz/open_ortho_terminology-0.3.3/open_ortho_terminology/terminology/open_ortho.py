""" open_ortho: a collection of static open-ortho.org codes.

Used whenever a code is necessary, for various implementations.
"""

from open_ortho_terminology.terminology import Code
from open_ortho_terminology.terminology.snomed import EV01, EV15, EV19
from open_ortho_terminology.terminology.vendors import OpenOrtho


def make_code(s):
    """
    Convert a string of ASCII characters to a single string of their equivalent integer values concatenated together.

    Args:
    s (str): A string to convert.

    Returns:
    str: A string consisting of the ASCII integer values concatenated together without any spaces.
    """
    # Convert each character to its ASCII integer, then to a string, and concatenate
    return ''.join(str(ord(char)) for char in s)


class OpenOrthoCode(Code):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prefix = OpenOrtho.PREFIX
        self.system = OpenOrtho.url


EV07 = OpenOrthoCode(
    code=f"{make_code('EV07')}",
    display="Extraoral, Right Profile (subject is facing observer's right), Mandible Postured Forward",
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['EV-07', 'EO.RP.MD.PF'])
""" Used for ... """

EV28 = OpenOrthoCode(
    code=f"{make_code('EV28')}",
    display="Extraoral, Left Profile (subject is facing observer's left), Mandible Postured Forward",
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['EV-28', 'EO.LP.MD.PF'])
""" Used for ... """

EV37 = OpenOrthoCode(
    code=f"{make_code('EV37')}",
    display="Extraoral, Other Face (viewed from above), Superior View (showing forehead, infraorbital rim contour, dorsum of nose, upper lip, chin)",
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['EV-37', 'EO.OF.SV'])

EV38 = OpenOrthoCode(
    code=f"{make_code('EV38')}",
    display="Extraoral, Other Face, Close-Up Smile (with lips)",
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['EV-38', 'EO.OF.CS'])

EV39 = OpenOrthoCode(
    code=f"{make_code('EV39')}",
    display="Extraoral, Other Face, Occlusal Cant (e.g., tongue depressor between the teeth)",
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['EV-39', 'EO.OF.OC'])

EV40 = OpenOrthoCode(
    code=f"{make_code('EV40')}",
    display="Extraoral, Other Face, Forensic Interest (tattoos, jewelry, scars)",
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['EV-40', 'EO.OF.FI'])

EV41 = OpenOrthoCode(
    code=f"{make_code('EV41')}",
    display="Extraoral, Other Face, Anomalies (ears, skin tags, etc.)",
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['EV-41', 'EO.OF.AN'])

EV42 = OpenOrthoCode(
    code=f"{make_code('EV42')}",
    display="Extraoral, Full Face, Mouth Open",
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['EV-42', 'EO.FF.MO'])

EV43 = OpenOrthoCode(
    code=f"{make_code('EV43')}",
    display="Extraoral, Full Face, demonstrating Nerve Weakness",
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['EV-43', 'EO.FF.NW'])

IV01 = OpenOrthoCode(
    code=f"{make_code('IV01')}",
    display='Intraoral Right Buccal Segment, Centric Occlusion, Direct View',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-01', 'IO.RB.CO', 'DEYE-brr'])
""" Used for ... """

IV02 = OpenOrthoCode(
    code=f"{make_code('IV02')}",
    display='Intraoral, Right Buccal Segment, Centric Occlusion, With Mirror',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-02', 'IO.RB.CO.WM'])
""" Used for ... """

IV03 = OpenOrthoCode(
    code=f"{make_code('IV03')}",
    display='Intraoral, Right Buccal Segment, Centric Occlusion, With Mirror, But Corrected',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-03', 'IO.RB.CO.WM.BC'])
""" Used for ... """

IV04 = OpenOrthoCode(
    code=f"{make_code('IV04')}",
    display='Intraoral, Right Buccal Segment, Centric Relation (Direct View)',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-04', 'IO.RB.CR'])
""" Used for ... """

IV05 = OpenOrthoCode(
    code=f"{make_code('IV05')}",
    display='Intraoral, Right Buccal Segment, Centric Relation, With Mirror',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-05', 'IO.RB.CR.WM'])
""" Used for ... """

IV06 = OpenOrthoCode(
    code=f"{make_code('IV06')}",
    display='Intraoral, Right Buccal Segment, Centric Relation, With Mirror, But Corrected',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-06', 'IO.RB.CR.WM.BC'])
""" Used for ... """

IV07 = OpenOrthoCode(
    code=f"{make_code('IV07')}",
    display='Intraoral, Frontal View, Centric Occlusion',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-07', 'IO.FV.CO', 'DEYE-frc'])
""" Used for ... """

IV08 = OpenOrthoCode(
    code=f"{make_code('IV08')}",
    display='Intraoral, Frontal View, Centric Relation',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-08', 'IO.FV.CR'])
""" Used for ... """

IV09 = OpenOrthoCode(
    code=f"{make_code('IV09')}",
    display='Intraoral, Frontal View, Teeth Apart',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-09', 'IO.FV.TA', 'DEYE-frg'])
""" Used for ... """

IV10 = OpenOrthoCode(
    code=f"{make_code('IV10')}",
    display='Intraoral, Frontal View, Mouth Open',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-10', 'IO.FV.MO'])
""" Used for ... """

IV11 = OpenOrthoCode(
    code=f"{make_code('IV11')}",
    display='Intraoral, Frontal View Inferior (showing depth of bite and overjet), Centric Occlusion',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-11', 'IO.FV.IV.CO'])
""" Used for ... """

IV12 = OpenOrthoCode(
    code=f"{make_code('IV12')}",
    display='Intraoral, Frontal View Inferior (showing depth of bite and overjet), Centric Relation',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-12', 'IO.FV.IV.CR'])
""" Used for ... """

IV13 = OpenOrthoCode(
    code=f"{make_code('IV13')}",
    display='Intraoral, Frontal View, showing Tongue Thrust',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-13', 'IO.FV.TT.NM'])
""" Used for ... """

IV14 = OpenOrthoCode(
    code=f"{make_code('IV14')}",
    display='Intraoral, Right Lateral View, Centric Occlusion, showing Overjet, (Direct View showing overjet from the side)',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-14', 'IO.RL.CO.OJ'])
""" Used for ... """

IV15 = OpenOrthoCode(
    code=f"{make_code('IV15')}",
    display='Intraoral, Right Lateral View, Centric Relation, showing Overjet (Direct View showing overjet from the side)',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-15', 'IO.RL.CR.OJ'])
""" Used for ... """

IV16 = OpenOrthoCode(
    code=f"{make_code('IV16')}",
    display='Intraoral, Left Lateral View, Centric Occlusion, showing Overjet, (Direct View showing overjet from the side)',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-16', 'IO.LL.CO.OJ'])
""" Used for ... """

IV17 = OpenOrthoCode(
    code=f"{make_code('IV17')}",
    display='Intraoral, Left Lateral View, Centric Relation, showing Overjet (Direct View showing overjet from the side)',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-17', 'IO.LL.CR.OJ'])
""" Used for ... """


IV18 = OpenOrthoCode(
    code=f"{make_code('IV18')}",
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    display='Intraoral, Left Buccal Segment, Centric Occlusion (Direct View)',
    synonyms=['IV-18', 'IO.LB.CO'])
""" Used for ... """


IV19 = OpenOrthoCode(
    code=f"{make_code('IV19')}",
    display='Intraoral, Left Buccal Segment, Centric Occlusion, With Mirror',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-19', 'IO.LB.CO.WM'])
""" Used for ... """


IV20 = OpenOrthoCode(
    code=f"{make_code('IV20')}",
    display='Intraoral, Left Buccal Segment, Centric Occlusion, With Mirror, But Corrected',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-20', 'IO.LB.CO.WM.BC'])
""" Used for ... """


IV21 = OpenOrthoCode(
    code=f"{make_code('IV21')}",
    display='Intraoral, Left Buccal Segment, Centric Relation (Direct View)',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-21', 'IO.LB.CR'])
""" Used for ... """


IV22 = OpenOrthoCode(
    code=f"{make_code('IV22')}",
    display='Intraoral, Left Buccal Segment, Centric Relation, With Mirror',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-22', 'IO.LB.CR.WM'])
""" Used for ... """


IV23 = OpenOrthoCode(
    code=f"{make_code('IV23')}",
    display='Intraoral, Left Buccal Segment, Centric Relation, With Mirror, But Corrected',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-23', 'IO.LB.CR.WM.BC'])
""" Used for ... """


IV24 = OpenOrthoCode(
    code=f"{make_code('IV24')}",
    display='Intraoral, Maxillary, Mouth Open, Occlusal View, With Mirror',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-24', 'IO.MX.MO.OV.WM'])
""" Used for ... """


IV25 = OpenOrthoCode(
    code=f"{make_code('IV25')}",
    display='Intraoral, Maxillary, Mouth Open, Occlusal View, With Mirror, But Corrected',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-25', 'IO.MX.MO.OV.WM.BC'])
""" Used for ... """


IV26 = OpenOrthoCode(
    code=f"{make_code('IV26')}",
    display='Intraoral, Mandibular, Mouth Open, Occlusal View, With Mirror',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-26', 'IO.MD.MO.OV.WM'])
""" Used for ... """


IV27 = OpenOrthoCode(
    code=f"{make_code('IV27')}",
    display='Intraoral, Mandibular, Mouth Open, Occlusal View, With Mirror, But Corrected',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-27', 'IO.MD.MO.OV.WM.BC'])
""" Used for ... """


IV28 = OpenOrthoCode(
    code=f"{make_code('IV28')}",
    display='Intraoral, showing Gingival Recession (ISO tooth numbers)',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-28', 'IO.GR.[tooth number]'])
""" Used for ... """


IV29 = OpenOrthoCode(
    code=f"{make_code('IV29')}",
    display='Intraoral, showing Frenum (ISO tooth numbers)',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-29', 'IO.FR.[tooth number]'])
""" Used for ... """


IV30 = OpenOrthoCode(
    code=f"{make_code('IV30')}",
    display='Intraoral, any photo using a photo accessory device (modifiers)',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProtocol'}],
    synonyms=['IV-30', 'IO.[modifier].PA'])
""" Used for ... """


VS01 = OpenOrthoCode(
    code=f"{make_code('VS01')}",
    display='ViewSet 01',
    contexts=[{'standard': 'DICOM', 'resource': 'ScheduledProcedureStep'}],
    synonyms=['VS-01', 'ABO'],
    expansion=[[EV01], [EV15], [EV19], [IV25], [None],
               [IV27], [IV01, IV03], [IV07], [IV18, IV20]]
)

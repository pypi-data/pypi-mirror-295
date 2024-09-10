import re
import difflib
from rapidfuzz import fuzz
from rapidfuzz import process

class ProcessingDecision() :    

    def __init__(self, part_column, pdf_column, pdfData ):
        self.part_column= part_column
        self.pdf_column= pdf_column
        self.pdfData= pdfData

    # Pre-compile regex exact
    def exactPattern(self, part):
        return re.compile(rf'(^|[\n ])(?P<k>[^\w]?{re.escape(part)}[^\w]?)([\n ]|$)', flags=re.IGNORECASE)
    # Pre-compile regex for dif fromat
    def difrPattern(self, part):
        return re.compile(rf'(^|[\n ])(?P<k>[\W_]*?{part}[\W_]*?)([\n ]|$)', flags=re.IGNORECASE)
    # Pre-compile regex for contains -
    def conatinsNegEndPattern(self, part):
        return re.compile(f'(^|[ \n])(?P<k>{re.escape(part)}.{{0,10}}?)($|[ \n])', flags=re.IGNORECASE)
    # Pre-compile regex for contains - S
    def conatinsNegStartPattern(self, part):
        return re.compile(f'(^|[ \n])(?P<k>.{{0,10}}?{re.escape(part)})($|[ \n])', flags=re.IGNORECASE)
    # Pre-compile regex for cotains +
    def conatinsPosStartPattern(self, part):
        half_length = int(len(part) / 2)
        start = re.sub('(\W)', r'(\\\1)?', part[:half_length] )
        start = re.sub('(\w)',r'\1?', start)
        end=  re.escape(part[half_length:])
        part= start + end
        return re.compile(f'(^|[ \n])(?P<k>{part})($|[ \n])', flags=re.IGNORECASE)
    # Pre-compile regex for cotains +
    def conatinsPosEndPattern(self, part):
        half_length = int(len(part) / 2)
        start= re.escape(part[:half_length])
        end = re.sub('(\W)', r'(\\\1)?', part[half_length:])
        end = re.sub('(\w)',r'\1?', end)
        part= start + end
        return re.compile(f'(^|[ \n])(?P<k>{part})($|[ \n])', flags=re.IGNORECASE)
    # Pre-compile regex for contains
    def conatinsPattern(self, part):
        return re.compile(rf'(^|[ \n])(?P<k>.{{0,10}}?{part}.{{0,10}}?)($|[ \n])', flags=re.IGNORECASE)
    
    def normalize_string(self, s):
        """Normalizes a string by removing non-word characters and converting to lowercase."""
        return re.sub(r'[\W_]', '', s).lower() 
    
    def find_Suffix_Positions_negative(self, part, matched_part):
        match_metrix={str(index+1):suffix[2:] for index,suffix in enumerate(difflib.ndiff(part, matched_part)) if suffix.startswith('+')}
        SUFFIXS= ''.join(match_metrix.values())
        POSITIONS= ','.join(match_metrix.keys()) 
        return SUFFIXS, POSITIONS
    
    def find_Suffix_Positions_positive(self, part, matched_part):
        match_metrix={str(index+1):suffix[2:] for index,suffix in enumerate(difflib.ndiff(part, matched_part)) if suffix.startswith('-')}
        SUFFIXS= ''.join(match_metrix.values())
        POSITIONS= ','.join(match_metrix.keys()) 
        return SUFFIXS, POSITIONS
    
    def matchFuzzy(self, part, pdf_data):
        matches = [match for match in process.extract(part, re.split('[\n ]',pdf_data), limit=5, scorer=fuzz.ratio)
                   if match[1]>=60]
        return matches
            

    def MakeDecision(self, row):

        pdf= row[self.pdf_column]
        part= row[self.part_column]

        if len(part) <=4 or str(pdf) not in self.pdfData:
            row[f'DECISION_{self.pdf_column}']=  'Need Check'
            return row
        
        pdf_data= ' '.join(self.pdfData[pdf])

        if len(pdf_data) <150:
            row[f'DECISION_{self.pdf_column}']= 'OCR'
            return row
        #look for Exact using regex
        exact_match = self.exactPattern(part).search(pdf_data)
        if exact_match:
            row[f'DECISION_{self.pdf_column}'] = 'EXACT'
            row[f'EQUIVALENT_{self.pdf_column}']= exact_match.group('k').strip()
            return row
        #look for dif format using regex
        sub_part= '[\W_]{0,3}?'.join(self.normalize_string(part))
        dif_match= self.difrPattern(sub_part).search(pdf_data)
        if dif_match:
            row[f'DECISION_{self.pdf_column}'] = 'DIF_FORMAT'
            row[f'EQUIVALENT_{self.pdf_column}']= dif_match.group('k').replace('\n',' ').strip()
            return row
        #Find if Part Conatins Negative
        contains_neg= self.conatinsNegStartPattern(part).search(pdf_data)
        if contains_neg:
            matched_part= contains_neg.group('k').replace('\n',' ').strip()
            row[f'DECISION_{self.pdf_column}'] = 'Conatins -'
            row[f'EQUIVALENT_{self.pdf_column}']= matched_part
            row[f'SUFFIXS_{self.pdf_column}'], row[f'POSITIONS_{self.pdf_column}'] = self.find_Suffix_Positions_negative(part, matched_part)
            return row
        contains_neg= self.conatinsNegEndPattern(part).search(pdf_data)
        if contains_neg:
            matched_part= contains_neg.group('k').replace('\n',' ').strip()
            row[f'DECISION_{self.pdf_column}'] = 'Conatins -'
            row[f'EQUIVALENT_{self.pdf_column}']= matched_part
            row[f'SUFFIXS_{self.pdf_column}'], row[f'POSITIONS_{self.pdf_column}'] = self.find_Suffix_Positions_negative(part, matched_part)
            return row
        #Find if Part Conatins positve
        contains_pos= {len(f.group('k').replace('\n',' ').strip()): f.group('k').replace('\n',' ').strip() for f in self.conatinsPosStartPattern(part).finditer(pdf_data) if f}
        if contains_pos:
            matched_part= contains_pos[max(contains_pos.keys())]
            row[f'DECISION_{self.pdf_column}'] = 'Conatins +'
            row[f'EQUIVALENT_{self.pdf_column}']= matched_part
            row[f'SUFFIXS_{self.pdf_column}'], row[f'POSITIONS_{self.pdf_column}'] = self.find_Suffix_Positions_positive(part, matched_part)
            return row
        contains_pos= {len(f.group('k').replace('\n',' ').strip()):f.group('k').replace('\n',' ').strip() for f in self.conatinsPosEndPattern(part).finditer(pdf_data) if f}
        if contains_pos:
            matched_part= contains_pos[max(contains_pos.keys())]
            row[f'DECISION_{self.pdf_column}'] = 'Conatins +'
            row[f'EQUIVALENT_{self.pdf_column}']= matched_part
            row[f'SUFFIXS_{self.pdf_column}'], row[f'POSITIONS_{self.pdf_column}'] = self.find_Suffix_Positions_positive(part, matched_part)
            return row
        #Find if Part Conatins
        contains= self.conatinsPattern(sub_part).search(pdf_data)
        if contains:
            row[f'DECISION_{self.pdf_column}'] = 'Conatins'
            row[f'EQUIVALENT_{self.pdf_column}']= contains.group('k').replace('\n',' ').strip()
            return row
        #matches using fuzzy
        fuzz_match= self.matchFuzzy(part, pdf_data)
        if fuzz_match and fuzz_match[0][0].lower() in part.lower():
            row[f'DECISION_{self.pdf_column}'] = 'Conatins +'
            row[f'EQUIVALENT_{self.pdf_column}']= fuzz_match[0][0]
            row[f'SUFFIXS_{self.pdf_column}'], row[f'POSITIONS_{self.pdf_column}'] = self.find_Suffix_Positions_positive(part, fuzz_match[0][0])
            return row
        elif fuzz_match and part.lower() in fuzz_match[0][0].lower():
            row[f'DECISION_{self.pdf_column}'] = 'Conatins -'
            row[f'EQUIVALENT_{self.pdf_column}']= fuzz_match[0][0]
            row[f'SUFFIXS_{self.pdf_column}'], row[f'POSITIONS_{self.pdf_column}'] = self.find_Suffix_Positions_negative(part, fuzz_match[0][0])
        elif fuzz_match:
            row[f'DECISION_{self.pdf_column}'] = 'Need Check'
            row[f'EQUIVALENT_{self.pdf_column}']= fuzz_match[0][0]
        else:
            row[f'DECISION_{self.pdf_column}'] = 'Need Check'
        return row
    

    
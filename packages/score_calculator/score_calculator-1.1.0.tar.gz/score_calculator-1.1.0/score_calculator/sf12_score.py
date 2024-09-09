import pandas as pd
import numpy as np
from score_calculator.sf12_utils import coalesce, recode, extract


class SF12Score:
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.answers = None
        
    def calculate_f12_score(self):
        pass 
    def __load_csv_to_dataframe(self, file_path):
        """
        Loads a CSV file into a pandas DataFrame.

        Args:
            file_path: The path to the CSV file.

        Returns:
            A pandas DataFrame containing the data from the CSV file.
        """
        try:
            df = pd.read_csv(file_path)
            return df
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            return None
        except pd.errors.EmptyDataError:
            print(f"Error: No data found in {file_path}")
            return None
        except Exception as e:
            print(f"An error occurred while reading the CSV: {e}")
            return None
    
    """Load the answers from the file
    file_path: str, the path to the file containing the answers
    """
    def load_answers(self):
        # Load CSV file
        self.answers = self.__load_csv_to_dataframe(self.file_path)
        # Convert keys to lower case
        self.answers.columns = [col.lower() for col in self.answers.columns]
        return self.answers
    
    def __get_column_names(self, required_names=None):
        names = []
        for col in ["vt2", "mh3", "mh4"]:
            for i in range(1, 7): 
                if col in required_names:
                    names.append(f"{col}_{i}")
                
        # Step 2: Create Indicator Variables
        for col in ["pf02", "pf04"]:
            for i in range(1, 4):
                if col in required_names:
                    names.append(f"{col}_{i}")
        
        for col in ["rp2", "rp3", "re2", "re3"]:
            if col in required_names:
                names.append(f"{col}_1")

        for col in ["bp2", "gh1", "sf2"]:
            for i in range(1, 6):  
                if col in required_names:
                    names.append(f"{col}_{i}")
        return names
    
    def __populate_column_names(self, eprocess_dataclude_column, arr=None):
        names = []
        for col in ["vt2", "mh3", "mh4"]:
            for i in range(1, 7): 
                if col != eprocess_dataclude_column:
                    names.append(f"{col}_{i}")
                    arr[f"{col}_{i}"] = 0
 
                
        # Step 2: Create Indicator Variables
        for col in ["pf02", "pf04"]:
            for i in range(1, 4):
                if col != eprocess_dataclude_column:
                    names.append(f"{col}_{i}")
                    arr[f"{col}_{i}"] = 0
    
        for col in ["rp2", "rp3", "re2", "re3"]:
            if col != eprocess_dataclude_column:
                names.append(f"{col}_1")
                arr[f"{col}_1"] = 0

        for col in ["bp2", "gh1", "sf2"]:
            
            for i in range(1, 6):  
                if col != eprocess_dataclude_column:
                    names.append(f"{col}_{i}")
                    arr[f"{col}_{i}"] = 0
        return arr
    import re

    def __replace_values(self):
        replacements = {
            "GH1": "Q1",
            "PF02": "Q2",
            "PF04": "Q3",
            "RP2": "Q4",
            "RP3": "Q5",
            "RE2": "Q6",
            "RE3": "Q7",
            "BP2": "Q8",
            "MH3": "Q9",
            "VT2": "Q10",
            "MH4": "Q11",
            "SF2": "Q12"
        }
        return replacements

    def sf12(self, input_data):
        """
        Scores the SF12 questionnaire.
        """
        return self.sf12_v1(input_data)
    
    # ported from https://github.com/uo-cmor/SF6Dvalues
    def sf12_v2(self, input_data):

        #rename keys of dict to match the expected keys
        input_data = {self.__replace_values()[k]: v for k, v in input_data.items()}
        # Rename the columns
        #input_data = input_data.rename(columns=self.__replace_values())
        dom_data = self.SF12_domains(input_data)
        final_score = self.calculate_final_score(dom_data)
        final_score_mcs = self.calculate_mcs_score(dom_data)
        return (final_score, final_score_mcs, dom_data)
    
    def SF12_domains(self, x):
        """Calculate SF-12 domains.

        Args:
            x: SF-12 data (assuming a dictionary-like structure)

        Returns:
            A dictionary containing calculated SF-12 domains.

        Raises:
            ValueError: If the SF-12 version is 1 (not supported).
        """

        if getattr(x, 'version', None) == 1:
            raise ValueError("SF-12 version 1 is not supported.")

            return mapping.get(value, value)  # Return original value if not found in mapping

        # Calculate domains (replace 'extract' with your data extraction logic)
        PF = ((coalesce(extract(x, "Q2"), extract(x, "Q3")) 
                + coalesce(extract(x, "Q3"), extract(x, "Q2")) - 2) / 4) * 100
        RP = ((coalesce(extract(x, "Q4"), extract(x, "Q5")) 
                + coalesce(extract(x, "Q5"), extract(x, "Q4")) - 2) / 8) * 100
        BP = ((6 - extract(x, "Q8") - 1) / 4) * 100
        GH = ((recode(extract(x, "Q1"), 5, 4.4, 3.4, 2, 1) - 1) / 4) * 100
        VT = ((6 - extract(x, "Q10") - 1) / 4) * 100
        SF = ((extract(x, "Q12") - 1) / 4) * 100
        RE = ((coalesce(extract(x, "Q6"), extract(x, "Q7")) 
                + coalesce(extract(x, "Q7"), extract(x, "Q6")) - 2) / 8) * 100
        MH = ((coalesce(6 - extract(x, "Q9"), extract(x, "Q11")) 
                + coalesce(extract(x, "Q11"), 6 - extract(x, "Q9")) - 2) / 8) * 100

        # Standardize domains
        PFz = (PF - 81.18122) / 29.10558
        RPz = (RP - 80.52856) / 27.13526
        BPz = (BP - 81.74015) / 24.53019
        GHz = (GH - 72.19795) / 23.19041
        VTz = (VT - 55.59090) / 24.84380
        SFz = (SF - 83.73973) / 24.75775
        REz = (RE - 86.41051) / 22.35543
        MHz = (MH - 70.18217) / 20.50597

        return {
            'PF': PF, 'RP': RP, 'BP': BP, 'GH': GH, 'VT': VT, 'SF': SF, 'RE': RE, 'MH': MH,
            'PFz': PFz, 'RPz': RPz, 'BPz': BPz, 'GHz': GHz, 'VTz': VTz, 'SFz': SFz, 'REz': REz, 'MHz': MHz
        }
        
    def calculate_final_score(self, dom):
        """Calculates the final score based on standardized SF-12 domain scores.

        Args:
            dom: A dictionary containing the standardized SF-12 domain scores 
                (PFz, RPz, BPz, GHz, VTz, SFz, REz, MHz).

        Returns:
            The calculated final score.
        """

        # Calculate the Physical Component Summary (PCS) score (PHYS)
        PHYS = (
            dom["PFz"] * 0.42402
            + dom["RPz"] * 0.35119
            + dom["BPz"] * 0.31754
            + dom["GHz"] * 0.24954
            + dom["VTz"] * 0.02877
            + dom["SFz"] * -0.00753
            + dom["REz"] * -0.19206
            + dom["MHz"] * -0.22069
        )

        # Calculate the final score by scaling and shifting the PCS score
        final_score = 50 + PHYS * 10

        return final_score

        # Example usage (replace with your actual 'dom' data)
        dom_data = {
            "PFz": 0.5,
            "RPz": 0.3,
            "BPz": 0.2,
            "GHz": 0.4,
            "VTz": 0.6,
            "SFz": 0.1,
            "REz": 0.7,
            "MHz": 0.8,
        }
    def calculate_mcs_score(self, dom):
        """Calculates the Mental Component Summary (MCS) score based on standardized SF-12 domain scores.

        Args:
            dom: A dictionary containing the standardized SF-12 domain scores 
                (PFz, RPz, BPz, GHz, VTz, SFz, REz, MHz).

        Returns:
            The calculated final MCS score.
        """

        # Calculate the Mental Component Summary (MCS) score (MENT)
        MENT = (
            dom["PFz"] * -0.22999
            + dom["RPz"] * -0.12329
            + dom["BPz"] * -0.09731
            + dom["GHz"] * -0.01571
            + dom["VTz"] * 0.23534
            + dom["SFz"] * 0.26876
            + dom["REz"] * 0.43407
            + dom["MHz"] * 0.48581
        )

        # Calculate the final MCS score by scaling and shifting the MENT score
        final_mcs_score = 50 + MENT * 10

        return final_mcs_score  
    def sf12_v1(self, input_data):
        """
        Scores the SF12 questionnaire.

        Args:
            process_data: A pandas DataFrame or NumPy array with 12 columns containing questionnaire items.
            Column order: GH1, PF02, PF04, RP2, RP3, RE2, RE3, BP2, MH3, VT2, MH4, SF2.

        Returns:
            A pandas DataFrame with two columns: PCS12 and MCS12.
        """

        if not isinstance(input_data, (pd.DataFrame, np.ndarray)) or input_data.shape[1] != 12:
            raise ValueError("process_data must be a DataFrame (or array) with 12 columns")
        input_data.columns = [col.lower() for col in input_data.columns]
        process_data = pd.DataFrame()
        
        input_data["bp2"] = 6 - input_data["bp2"]
        input_data["gh1"] = 6 - input_data["gh1"]
        input_data["vt2"] = 7 - input_data["vt2"]
        input_data["mh3"] = 7 - input_data["mh3"]
        

        for col in ["vt2", "mh3", "mh4"]:
            for i in range(1, 7): 
                process_data[f"{col}_{i}"] = (input_data[col] == i).astype(int)
        
        for col in ["pf02", "pf04"]:
            for i in range(1, 4):
                process_data[f"{col}_{i}"] = (input_data[col] == i).astype(int)
        
        for col in ["rp2", "rp3", "re2", "re3"]:
            process_data[f"{col}_1"] = (input_data[col] == 1).astype(int)

        for col in ["bp2", "gh1", "sf2"]:
            for i in range(1, 6):  
                process_data[f"{col}_{i}"] = (input_data[col] == i).astype(int)
                

 
        values_pcs12 = (
            (-7.23216 * process_data["pf02_1"]) + (-3.45555 * process_data["pf02_2"]) +
            (-6.24397 * process_data["pf04_1"]) + (-2.73557 * process_data["pf04_2"]) +
            (-4.61617 * process_data["rp2_1"]) + (-5.51747 * process_data["rp3_1"]) +
            (-11.25544 * process_data["bp2_1"]) + (-8.38063 * process_data["bp2_2"]) +
            (-6.50522 * process_data["bp2_3"]) + (-3.80130 * process_data["bp2_4"]) +
            (-8.37399 * process_data["gh1_1"]) + (-5.56461 * process_data["gh1_2"]) +
            (-3.02396 * process_data["gh1_3"]) + (-1.31872 * process_data["gh1_4"]) +
            (-2.44706 * process_data["vt2_1"]) + (-2.02168 * process_data["vt2_2"]) +
            (-1.61850 * process_data["vt2_3"]) + (-1.14387 * process_data["vt2_4"]) +
            (-0.42251 * process_data["vt2_5"]) + (-0.33682 * process_data["sf2_1"]) +
            (-0.94342 * process_data["sf2_2"]) + (-0.18043 * process_data["sf2_3"]) +
            (0.11038  * process_data["sf2_4"]) + (3.04365  * process_data["re2_1"]) +
            (2.32091  * process_data["re3_1"]) + (3.46638  * process_data["mh3_1"]) +
            (2.90426  * process_data["mh3_2"]) + (2.37241  * process_data["mh3_3"]) +
            (1.36689  * process_data["mh3_4"]) + (0.66514  * process_data["mh3_5"]) +
            (4.61446  * process_data["mh4_1"]) + (3.41593  * process_data["mh4_2"]) +
            (2.34247  * process_data["mh4_3"]) + (1.28044  * process_data["mh4_4"]) +
            (0.41188  * process_data["mh4_5"])
        )

        values_mcs12 = (
            (3.93115  * process_data["pf02_1"]) + (1.86840  * process_data["pf02_2"]) +
            (2.68282  * process_data["pf04_1"]) + (1.43103  * process_data["pf04_2"]) +
            (1.44060  * process_data["rp2_1"]) + (1.66968  * process_data["rp3_1"]) +
            (1.48619  * process_data["bp2_1"]) + (1.76691  * process_data["bp2_2"]) +
            (1.49384  * process_data["bp2_3"]) + (0.90384  * process_data["bp2_4"]) +
            (-1.71175 * process_data["gh1_1"]) + (-0.16891 * process_data["gh1_2"]) +
            (0.03482  * process_data["gh1_3"]) + (-0.06064 * process_data["gh1_4"]) +
            (-6.02409 * process_data["vt2_1"]) + (-4.88962 * process_data["vt2_2"]) +
            (-3.29805 * process_data["vt2_3"]) + (-1.65178 * process_data["vt2_4"]) +
            (-0.92057 * process_data["vt2_5"]) + (-6.29724 * process_data["sf2_1"]) +
            (-8.26066 * process_data["sf2_2"]) + (-5.63286 * process_data["sf2_3"]) +
            (-3.13896 * process_data["sf2_4"]) + (-6.82672 * process_data["re2_1"]) +
            (-5.69921 * process_data["re3_1"]) + (-10.19085* process_data["mh3_1"]) +
            (-7.92717 * process_data["mh3_2"]) + (-6.31121 * process_data["mh3_3"]) +
            (-4.09842 * process_data["mh3_4"]) + (-1.94949 * process_data["mh3_5"]) +
            (-16.15395* process_data["mh4_1"]) + (-10.77911* process_data["mh4_2"]) +
            (-8.09914* process_data["mh4_3"]) + (-4.59055* process_data["mh4_4"]) + 
            (-1.95934* process_data["mh4_5"])
        )
        # Assuming values_pcs12 is a tuple of tuples
        values_pcs12_series = pd.Series(values_pcs12)
        
        # Perform the addition
        PCS12_series = values_pcs12_series + 56.57706
        
        # Assuming values_mcs12 is a tuple of tuples
        values_mcs12_series = pd.Series(values_mcs12)
        MCS12_series = values_mcs12_series + 60.75781
        
        return (PCS12_series, MCS12_series)


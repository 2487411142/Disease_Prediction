class UserData:
    def __init__(self, data):
        self.data = data

    def get_age(self):
        age_choice = self.data["SRAGE_P1"]
        return f"Around {age_choice} years old"

    def get_gender(self):
        gender_choice = self.data["SRSEX"]
        if gender_choice == "1":
            return "Male"
        elif gender_choice == "2":
            return "Female"
        else:
            return "Unknown"

    def get_marital(self):
        marital_choice = self.data["MARIT"]
        if marital_choice == "0":
            return "Married"
        elif marital_choice == "1":
            return "Separated or divorced"
        elif marital_choice == "2":
            return "Never married"
        else:
            return "Unknown"

    def get_occupation(self):
        occupation_choice = self.data["OCCMAIN2"]
        occupation_dict = {
            "1": "Management, business, and financial",
            "2": "Computer, engineering, and science",
            "3": "Education, legal, community service, art",
            "4": "Healthcare practitioners and technical",
            "5": "Service occupations",
            "6": "Sales and related occupations",
            "7": "Office and administrative support",
            "8": "Farming, fishing, and forestry",
            "9": "Construction and extraction",
            "10":"Installation, maintenance, and repair",
            "11":"Production occupations",
            "12":"Transportation and material moving",
            "13":"Military specific occupations"
        }
        return occupation_dict.get(occupation_choice, "Unknown")

    def get_weight(self):
        weight = self.data["WGHTK_P"]
        return f"{weight} kg"

    def get_bmi(self):
        bmi_choice = self.data["RBMI"]
        if bmi_choice == "0":
            return "Underweight"
        elif bmi_choice == "1":
            return "Normal"
        elif bmi_choice == "2":
            return "Overweight"
        elif bmi_choice == "3":
            return "Obesity"
        else:
            return "Unknown"

    def get_cigarette_freq(self):
        cigarette_freq_choice = self.data["AC174"]
        return f"Average {cigarette_freq_choice} days per month"

    def get_last_drink(self):
        last_drink_choice = self.data["AC208"]
        if last_drink_choice == "0":
            return "Within the past 30 days"
        elif last_drink_choice == "1":
            return "More than 30 days ago"
        elif last_drink_choice == "2":
            return "More than 12 months ago"
        elif last_drink_choice == "3":
            return "Never drank alcohol"
        else:
            return "Unknown"

    def get_physical_activity(self):
        physical_activity_choice = self.data["AC212"]
        if physical_activity_choice == "1":
            return "Yes"
        elif physical_activity_choice == "2":
            return "No"
        else:
            return "Unknown"

    def get_num_cigarettes_per_day(self):
        num_cigarettes_per_day_choice = self.data["NUMCIG"]
        if num_cigarettes_per_day_choice == "1":
            return "None"
        elif num_cigarettes_per_day_choice == "2":
            return "1"
        elif num_cigarettes_per_day_choice == "3":
            return "2-5"
        elif num_cigarettes_per_day_choice == "4":
            return "6-10"
        elif num_cigarettes_per_day_choice == "5":
            return "11-19"
        elif num_cigarettes_per_day_choice == "6":
            return "20 or more"

    def get_binge_drinking(self):
        binge_drinking_choice = self.data["BINGE30"]
        if binge_drinking_choice == "1":
            return "Yes"
        elif binge_drinking_choice == "2":
            return "No"
        else:
            return "Unknown"

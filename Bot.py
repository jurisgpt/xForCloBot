# Define the questionnaire with questions and weights
questionnaire = {
    "Core Information (CI)": {
        "Name": 1,
        "Phone number": 1,
        "Email address": 1,
        "User/Applicant Requests Anonymity": 1,
        "Postal Address": 1
    },
    "Property Ownership (PO)": {
        "Are you the Property owner?": 6,
        "If not the property owner, what is your relationship to the property owner": 5,
        "Would you like us to keep the Property owner be contacted on this matter?": 1,
        "If property owner would like to receive email update on this matter, please provide email address": 1,
        "What is the preferred method of contact for the property owner? Phone/Email/Postal Mail": 1,
        # Add more questions here
    },
    "Foreclosure Process (FP)": {
        "Property address that was foreclosed": 4,
        "Date of foreclosure sale": 4,
        "Name of lender/mortgage servicer": 2,
        # Add more questions here
    },
    "Property Advertisment (Property_Ad)": {
        "Describe the methods used by lender to advertise the property for sale?": 2,
        "Were these advertising methods explicitly laid out in the terms of the loan agreement or any other contractual instrument?": 1,
        # Add more questions here
    },
    "Property Sale (Property_Sale)": {
        "How did you determine the initial asking price of the property, and was this in line with market rates?": 1,
        "Was the sale open to the public, and if so, were reasonable steps taken to invite competitive bids?": 1,
        # Add more questions here
    },
    "Good Faith (GF)": {
        "At any point, was there any conflict of interest in conducting the sale?": 1,
        "Can you provide any evidence to support that the lender or lenders representative have acted impartially or not acted in good faith throughout the sales process?": 1,
        # Add more questions here
    }
}

def ask_questions_and_calculate_score(questionnaire):
    total_score = 0
    for section, questions in questionnaire.items():
        print(f"Section: {section}")
        for question, weight in questions.items():
            response = input(f"{question} (Affirmative/Provided/Negative/Not Provided/Neutral/Not sure/I don't understand this question): ")
            # You can add logic to handle different responses and assign scores accordingly
            if response != "":
                total_score += weight
            elif response == "":
                total_score -= weight
            # Handle other response types here

    return total_score

applicant_score = ask_questions_and_calculate_score(questionnaire)
print(f"Total Score: {applicant_score}")
if applicant_score > 0:
    print("Applicant is likely to be eligible for loan.")
elif applicant_score < 0:
    print("Applicant is likely to be ineligible for loan.")



rawinput = input()
  

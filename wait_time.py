from enum import Enum
from typing import List, Optional, Tuple


class Symptoms(Enum):
    FEVER = "fever"
    COUGH = "cough"
    HEART = "heart"
    OTHER = "other"

    def __str__(self):
        return self.value.capitalize()


class UrgencyLevel(Enum):
    MILD = 1
    MODERATE = 2
    SEVERE = 3


class Hospital:
    def __init__(self, name: str, specialty: Symptoms, patients: int, wait_time_per_patient: int):
        self.name = name
        self.specialty = specialty
        self.patients = patients
        self.wait_time_per_patient = wait_time_per_patient

    def add_patient(self) -> None:
        self.patients += 1

    def remove_patient(self) -> None:
        if self.patients > 0:
            self.patients -= 1

    def internal_wait_time(self, urgency: UrgencyLevel) -> float:
        if urgency.value == 0:
            raise ValueError("Urgency level cannot be 0")
        return round((self.patients * self.wait_time_per_patient) / urgency.value, 1)


def ask_for_symptoms() -> Symptoms:
    while True:
        print("Please enter your most severe symptom (fever, cough, heart, other):")
        symptoms = input().lower().strip()
        try:
            return Symptoms(symptoms)
        except ValueError:
            print("Invalid symptom. Valid options: fever, cough, heart, other")


def prompt_for_name() -> str:
    while True:
        print("Enter your name:")
        name = input().strip()
        if name:
            return name
        if name == "":
            print("Name cannot be empty")
        else:
            print("Invalid name")

def prompt_for_urgency_level() -> UrgencyLevel:
    while True:
        print("Please enter your urgency level (1: Mild, 2: Moderate, 3: Severe):")
        try:
            urgency = int(input().strip())
            if urgency in [1, 2, 3]:
                return UrgencyLevel(urgency)
            print("Invalid urgency level. Enter 1, 2, or 3")
        except ValueError:
            print("Invalid urgency level. Enter 1, 2, or 3")


def find_specialty_hospital(hospitals: List[Hospital], symptom: Symptoms) -> Optional[Hospital]:
    for hospital in hospitals:
        if hospital.specialty == symptom:
            return hospital
    return None


def find_fastest_hospital(hospitals: List[Hospital], urgency: UrgencyLevel) -> Tuple[Hospital, float]:
    wait_times = [(hospital, hospital.internal_wait_time(urgency)) for hospital in hospitals]
    return min(wait_times, key=lambda x: x[1])


def print_results(
        name: str,
        symptoms: Symptoms,
        urgency: UrgencyLevel,
        hospitals: List[Hospital]
) -> None:
    print("--- Results ---")
    print(f"Patient Name: {name}")
    print(f"Symptoms: {symptoms.value}")
    print(f"Urgency Level: {urgency.value}")

    # Calculate and display wait times for all hospitals
    for hospital in hospitals:
        wait_time = hospital.internal_wait_time(urgency)
        print(f"{hospital.name} Wait Time: {wait_time} minutes")

    # Find specialty and fastest hospitals
    fastest_hospital, fastest_time = find_fastest_hospital(hospitals, urgency)

    # Print recommendation based on symptoms
    print()  # Empty line before recommendation
    if symptoms != Symptoms.OTHER:
        specialty_hospital = find_specialty_hospital(hospitals, symptoms)
        if specialty_hospital:
            specialty_time = specialty_hospital.internal_wait_time(urgency)
            time_difference = abs(round(specialty_time - fastest_time, 1))
            print(f"Specialty hospital wait time: {specialty_time} minutes")
            print(f"Fastest hospital: {fastest_hospital.name} with {fastest_time} minutes")
            print(f"Difference: {time_difference} minutes")
    else:
        print(f"Fastest hospital: {fastest_hospital.name} with {fastest_time} minutes")
        print("No specialty hospital for your symptom.")


def main():
    # Initialize hospitals with correct names
    victoria = Hospital("Victoria Hospital", Symptoms.FEVER, 15, 10)
    joseph = Hospital("St. Joseph's Hospital", Symptoms.COUGH, 10, 12)
    london_health = Hospital("London Health Sciences Centre", Symptoms.HEART, 20, 8)

    hospitals = [victoria, joseph, london_health]

    # Get patient information
    name = prompt_for_name()
    symptoms = ask_for_symptoms()
    urgency = prompt_for_urgency_level()

    # Print results in required format
    print_results(name, symptoms, urgency, hospitals)


if __name__ == '__main__':
    main()

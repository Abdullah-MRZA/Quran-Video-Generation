import text
import questionary
import network_requests


def get_user_translation_desire() -> network_requests.translator:
    translations = network_requests.get_translations()
    selection: str = questionary.select(
        message="Which of these translations do you want to use?",
        choices=[x.translation_name for x in translations],
    ).ask()

    return [x for x in translations if x.translation_name == selection][0]


def main():
    reciter: str = ""
    # translations: list[str] = []

    # translations = questionary.checkbox(

    translations = get_user_translation_desire()
    print(translations)

    # surah_number = questionary.autocomplete(message="Which surah?", choices=)

    # Then some way to customise the video process itself, eg with the different colour themes,
    # changing the layout / resolution

    # Also... MEMORY-EFFICIENT RENDERER is very important


if __name__ == "__main__":
    main()

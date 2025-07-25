import text
import questionary
import network_requests


def main():
    reciter: str = ""
    translations: list[str] = []

    # translations = questionary.checkbox(
    translations = questionary.select(
        message="Which of these translations do you want to use?",
        choices=[x.translation_name for x in network_requests.get_translations()],
    ).ask()

    # surah_number = questionary.autocomplete(message="Which surah?", choices=)

    # Then some way to customise the video process itself, eg with the different colour themes,
    # changing the layout / resolution

    # Also... MEMORY-EFFICIENT RENDERER is very important


if __name__ == "__main__":
    main()

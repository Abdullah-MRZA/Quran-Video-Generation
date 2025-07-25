from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    field_validator,
    validate_call,
)


class WordByWord(BaseModel):
    arabic: str = Field(..., description="Individual Arabic word", min_length=1)
    english: str = Field(..., description="Word-by-word English gloss", min_length=1)
    translation_type: str = Field(..., description="Name of the translation type")

    @field_validator("english", mode="before")
    def clean_english(cls, v: str) -> str:
        # strip whitespace, normalize quotes, collapse multiple spaces
        text = v.strip()
        text = text.replace("“", '"').replace("”", '"').replace("’", "'")
        return " ".join(text.split())


class Translation(BaseModel):
    text: str = Field(..., description="Full English translation", min_length=1)
    translator: str = Field(..., description="Name or type of the translation")

    @field_validator("text", mode="before")
    def clean_text(cls, v: str) -> str:
        t = v.strip()
        t = t.replace("“", '"').replace("”", '"').replace("’", "'")
        return " ".join(t.split())

    @field_validator("translator", mode="before")
    def clean_translator(cls, v: str) -> str:
        return v.strip()


class Ayah(BaseModel):
    surah: int = Field(..., ge=1, description="Surah (chapter) number")
    ayah: int = Field(..., ge=1, description="Ayah (verse) number within the surah")
    arabic_text: str = Field(
        ..., description="Full Arabic text of the ayah", min_length=1
    )
    translation: Translation | None = Field(
        None, description="Full English translation with translator info"
    )
    audio_url: HttpUrl | None = Field(
        None, description="Direct link to the ayah’s audio file"
    )
    audio_timestamp: float | None = Field(
        None, ge=0, description="Timestamp (seconds) within a surah-long audio"
    )
    word_by_word: list[WordByWord] | None = Field(
        None, description="List of individual word translations"
    )

    @validate_call
    def validate_audio_fields(cls, values: dict[str, str | int | None]):
        url, ts = values.get("audio_url"), values.get("audio_timestamp")
        if url and ts is not None:
            raise ValueError("Provide either audio_url or audio_timestamp, not both")
        return values

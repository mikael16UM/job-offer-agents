from typing import Literal

from pydantic import BaseModel, Field


class JobOffer(BaseModel):
    """Oferta de empleo ya estructurada: lo que devuelve el agente Extractor.

    Es el contrato de datos entre el Extractor y el siguiente agente.
    Las descripciones de cada Field no son decoración: LangChain se las
    envía al modelo como instrucciones de qué poner en cada campo.
    """

    title: str = Field(description="Título del puesto tal como aparece en la oferta")

    # None permite que el modelo diga "no viene" en vez de inventar un dato
    company: str | None = Field(
        default=None, description="Nombre de la empresa. None si no se menciona"
    )

    # Literal restringe los valores válidos: el modelo no puede salirse de la lista
    seniority: Literal["junior", "mid", "senior", "lead", "not_specified"] = Field(
        description="Nivel del puesto. 'not_specified' si la oferta no lo indica"
    )

    required_skills: list[str] = Field(
        description="Tecnologías y habilidades obligatorias, una por elemento"
    )

    nice_to_have_skills: list[str] = Field(
        default_factory=list,
        description="Tecnologías o habilidades deseables pero no obligatorias",
    )

    years_experience: int | None = Field(
        default=None,
        description="Años mínimos de experiencia pedidos. None si no se indican",
    )

    modality: Literal["remote", "hybrid", "onsite", "not_specified"] = Field(
        description="Modalidad de trabajo. 'not_specified' si no se indica"
    )

    summary: str = Field(
        description="Resumen de la oferta en máximo dos frases, en español"
    )
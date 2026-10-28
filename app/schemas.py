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

class CandidateProfile(BaseModel):
    """Perfil estructurado extraído de un CV: salida del agente B.

    Decisión de diseño: este schema NO tiene campos de nombre, correo,
    teléfono ni dirección. Para comparar un CV con una vacante no hacen
    falta, y no extraerlos reduce el manejo de datos personales.
    """

    current_title: str | None = Field(
        default=None,
        description="Puesto actual o más reciente. None si no se indica",
    )

    years_experience: int | None = Field(
        default=None,
        description="Años totales de experiencia profesional que el CV permite "
        "sustentar. None si no se puede determinar",
    )

    skills: list[str] = Field(
        description="Tecnologías y habilidades que el CV menciona explícitamente, "
        "una por elemento"
    )

    experience_highlights: list[str] = Field(
        description="Máximo 5 logros o responsabilidades clave, en una frase cada una"
    )

    education: list[str] = Field(
        default_factory=list,
        description="Formación académica y certificaciones relevantes",
    )

    languages: list[str] = Field(
        default_factory=list,
        description="Idiomas mencionados, con nivel si se indica",
    )

    summary: str = Field(
        description="Resumen del perfil en máximo dos frases, en español"
    )


class MatchReport(BaseModel):
    """Resultado de comparar vacante y candidato: salida del agente C."""

    score: int = Field(
        ge=0, le=100,
        description="Compatibilidad global de 0 a 100, justificada por los demás campos",
    )

    verdict: str = Field(
        description="Veredicto en máximo dos frases, en español"
    )

    matched_required_skills: list[str] = Field(
        description="Habilidades obligatorias de la vacante que el candidato sí tiene"
    )

    missing_required_skills: list[str] = Field(
        description="Habilidades obligatorias de la vacante que el candidato no muestra"
    )

    strengths: list[str] = Field(
        description="Puntos fuertes del candidato frente a esta vacante"
    )

    gaps: list[str] = Field(
        description="Brechas importantes frente a lo que pide la vacante"
    )

    recommendations: list[str] = Field(
        description="Acciones concretas para mejorar el encaje (qué reforzar o destacar)"
    )


class AnalysisMeta(BaseModel):
    """Metadatos de la ejecución, útiles para transparencia en el demo."""

    mode: Literal["demo", "live"] = Field(
        description="'demo' si es un resultado pregrabado, 'live' si corrió en vivo"
    )
    model: str | None = Field(
        default=None, description="Modelo que generó el resultado"
    )
    duration_ms: int | None = Field(
        default=None, description="Duración total del análisis en milisegundos"
    )


class AnalysisResponse(BaseModel):
    """Respuesta completa de la API: lo que recibe la página web."""

    job: JobOffer
    candidate: CandidateProfile
    match: MatchReport
    meta: AnalysisMeta
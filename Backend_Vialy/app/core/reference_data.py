"""
Datos de referencia del Código Nacional de Tránsito Colombiano
Valores actualizados para 2025 según Artículo 131
"""

# SMMLV 2025 (Salario Mínimo Mensual Legal Vigente)
SMMLV_2025 = 1_423_500

# SMLDV = SMMLV / 30 (Salario Mínimo Legal Diario Vigente)
SMLDV_2025 = SMMLV_2025 / 30  # = $47,450

# Tipos de multas según Artículo 131 y sus valores
MULTAS_TIPOS = {
    'A': {
        'smldv': 4,
        'pesos': int(SMLDV_2025 * 4),  # $189,800
        'valor_texto': '$189,800',
        'descripcion': 'Vehículos no automotores o tracción animal'
    },
    'B': {
        'smldv': 8,
        'pesos': int(SMLDV_2025 * 8),  # $379,600
        'valor_texto': '$379,600',
        'descripcion': 'Infracciones leves'
    },
    'C': {
        'smldv': 15,
        'pesos': int(SMLDV_2025 * 15),  # $711,750
        'valor_texto': '$711,750',
        'descripcion': 'Infracciones moderadas'
    },
    'D': {
        'smldv': 30,
        'pesos': int(SMLDV_2025 * 30),  # $1,423,500
        'valor_texto': '$1,423,500',
        'descripcion': 'Infracciones graves'
    },
    'E': {
        'smldv': 45,
        'pesos': int(SMLDV_2025 * 45),  # $2,135,250
        'valor_texto': '$2,135,250',
        'descripcion': 'Infracciones muy graves'
    }
}

# Infracciones comunes según el Código (Artículo 131)
INFRACCIONES_COMUNES = {
    'exceso_velocidad': {
        'descripcion': 'Conducir a velocidad superior a la máxima permitida (C.29)',
        'tipo_multa': 'C',
        'valor': MULTAS_TIPOS['C']['pesos'],
        'articulo': '131-C.29',
        'otras_sanciones': []
    },
    'conducir_sin_licencia': {
        'descripcion': 'Guiar un vehículo sin licencia de conducción (D.1)',
        'tipo_multa': 'D',
        'valor': MULTAS_TIPOS['D']['pesos'],
        'articulo': '131-D.1',
        'otras_sanciones': ['Inmovilización del vehículo']
    },
    'no_cinturon': {
        'descripcion': 'No utilizar cinturón de seguridad (C.6)',
        'tipo_multa': 'C',
        'valor': MULTAS_TIPOS['C']['pesos'],
        'articulo': '131-C.6',
        'otras_sanciones': []
    },
    'semaforo_rojo': {
        'descripcion': 'No detenerse ante luz roja o señal de PARE (D.4)',
        'tipo_multa': 'D',
        'valor': MULTAS_TIPOS['D']['pesos'],
        'articulo': '131-D.4',
        'otras_sanciones': ['Inmovilización (motos)']
    },
    'conducir_embriagado': {
        'descripcion': 'Conducir bajo efectos del alcohol (F - Art. 152)',
        'tipo_multa': 'F',
        'valor': None,  # Se establece en artículo 152
        'articulo': '131-F / Art. 152',
        'otras_sanciones': [
            'Suspensión de licencia',
            'Inmovilización del vehículo',
            'Multa según nivel de alcoholemia'
        ]
    },
    'no_soat': {
        'descripcion': 'Conducir sin portar SOAT (D.2)',
        'tipo_multa': 'D',
        'valor': MULTAS_TIPOS['D']['pesos'],
        'articulo': '131-D.2',
        'otras_sanciones': ['Inmovilización del vehículo']
    },
    'celular_conduciendo': {
        'descripcion': 'Usar celular mientras conduce sin manos libres (C.38)',
        'tipo_multa': 'C',
        'valor': MULTAS_TIPOS['C']['pesos'],
        'articulo': '131-C.38',
        'otras_sanciones': []
    },
    'estacionar_prohibido': {
        'descripcion': 'Estacionar en sitios prohibidos (C.2)',
        'tipo_multa': 'C',
        'valor': MULTAS_TIPOS['C']['pesos'],
        'articulo': '131-C.2',
        'otras_sanciones': []
    },
    'sin_licencia_porte': {
        'descripcion': 'Conducir sin llevar consigo la licencia (B.1)',
        'tipo_multa': 'B',
        'valor': MULTAS_TIPOS['B']['pesos'],
        'articulo': '131-B.1',
        'otras_sanciones': []
    },
    'sentido_contrario': {
        'descripcion': 'Transitar en sentido contrario (D.3)',
        'tipo_multa': 'D',
        'valor': MULTAS_TIPOS['D']['pesos'],
        'articulo': '131-D.3',
        'otras_sanciones': ['Inmovilización (motos)']
    },
    'maniobras_peligrosas': {
        'descripcion': 'Maniobras altamente peligrosas (D.7)',
        'tipo_multa': 'D',
        'valor': MULTAS_TIPOS['D']['pesos'],
        'articulo': '131-D.7',
        'otras_sanciones': ['Inmovilización (motos)']
    },
    'revision_tecnomecanica': {
        'descripcion': 'No realizar revisión técnico-mecánica (C.35)',
        'tipo_multa': 'C',
        'valor': MULTAS_TIPOS['C']['pesos'],
        'articulo': '131-C.35',
        'otras_sanciones': ['Inmovilización del vehículo']
    }
}

# Documentos obligatorios
DOCUMENTOS_OBLIGATORIOS = [
    {
        'nombre': 'Licencia de conducción',
        'descripcion': 'Vigente y correspondiente a la categoría del vehículo',
        'obligatorio': True
    },
    {
        'nombre': 'Documento de identidad',
        'descripcion': 'Cédula de ciudadanía o extranjería',
        'obligatorio': True
    },
    {
        'nombre': 'SOAT',
        'descripcion': 'Seguro Obligatorio de Accidentes de Tránsito vigente',
        'obligatorio': True
    },
    {
        'nombre': 'Tarjeta de propiedad',
        'descripcion': 'Documento de propiedad del vehículo',
        'obligatorio': True
    },
    {
        'nombre': 'Certificado de revisión técnico-mecánica',
        'descripcion': 'Para vehículos particulares de más de 2 años',
        'obligatorio': True
    }
]

# Costos aproximados 2025
COSTOS_TRAMITES = {
    'licencia_nueva': {
        'min': 350_000,
        'max': 500_000,
        'descripcion': 'Obtener licencia nueva por primera vez'
    },
    'renovacion_licencia': {
        'min': 200_000,
        'max': 300_000,
        'descripcion': 'Renovación de licencia de conducción'
    },
    'soat_moto': {
        'min': 350_000,
        'max': 450_000,
        'descripcion': 'SOAT para motocicleta'
    },
    'soat_carro': {
        'min': 500_000,
        'max': 800_000,
        'descripcion': 'SOAT para automóvil'
    },
    'revision_tecnomecanica': {
        'min': 70_000,
        'max': 150_000,
        'descripcion': 'Revisión técnico-mecánica'
    },
    'examen_medico': {
        'min': 40_000,
        'max': 80_000,
        'descripcion': 'Examen médico para licencia'
    },
    'curso_conduccion': {
        'min': 800_000,
        'max': 1_500_000,
        'descripcion': 'Curso de conducción completo'
    }
}

# Límites de velocidad
LIMITES_VELOCIDAD = {
    'zona_escolar': 30,
    'zona_residencial': 30,
    'zona_urbana': 50,
    'zona_rural': 80,
    'autopista': 100,
    'autopista_doble_calzada': 120
}

def get_multa_info(tipo: str) -> dict:
    """
    Obtiene información de una multa por tipo
    
    Args:
        tipo: Tipo de multa (A, B, C, D, E)
        
    Returns:
        dict: Información de la multa
    """
    return MULTAS_TIPOS.get(tipo.upper(), None)

def get_infraccion_info(key: str) -> dict:
    """
    Obtiene información de una infracción específica
    
    Args:
        key: Clave de la infracción
        
    Returns:
        dict: Información de la infracción
    """
    return INFRACCIONES_COMUNES.get(key, None)

def format_pesos(valor: int) -> str:
    """
    Formatea un valor en pesos colombianos
    
    Args:
        valor: Valor numérico
        
    Returns:
        str: Valor formateado (ej: $1,423,500)
    """
    return f"${valor:,}".replace(',', '.')

def buscar_infraccion_por_keyword(keyword: str) -> list:
    """
    Busca infracciones que coincidan con una palabra clave
    
    Args:
        keyword: Palabra a buscar
        
    Returns:
        list: Lista de infracciones que coinciden
    """
    keyword = keyword.lower()
    resultados = []
    
    for key, info in INFRACCIONES_COMUNES.items():
        if keyword in info['descripcion'].lower() or keyword in key:
            resultados.append({
                'key': key,
                'info': info
            })
    
    return resultados

# Documentos obligatorios
DOCUMENTOS_OBLIGATORIOS = [
    {
        'nombre': 'Licencia de conducción',
        'descripcion': 'Vigente y correspondiente a la categoría del vehículo',
        'obligatorio': True
    },
    {
        'nombre': 'Documento de identidad',
        'descripcion': 'Cédula de ciudadanía o extranjería',
        'obligatorio': True
    },
    {
        'nombre': 'SOAT',
        'descripcion': 'Seguro Obligatorio de Accidentes de Tránsito vigente',
        'obligatorio': True
    },
    {
        'nombre': 'Tarjeta de propiedad',
        'descripcion': 'Documento de propiedad del vehículo',
        'obligatorio': True
    },
    {
        'nombre': 'Certificado de revisión técnico-mecánica',
        'descripcion': 'Para vehículos de más de 2 años (particulares) o 1 año (públicos)',
        'obligatorio': True
    }
]

# Costos aproximados 2025
COSTOS_TRAMITES = {
    'licencia_nueva': {
        'min': 350_000,
        'max': 500_000,
        'descripcion': 'Obtener licencia nueva por primera vez'
    },
    'renovacion_licencia': {
        'min': 200_000,
        'max': 300_000,
        'descripcion': 'Renovación de licencia de conducción'
    },
    'soat_moto': {
        'min': 350_000,
        'max': 450_000,
        'descripcion': 'SOAT para motocicleta'
    },
    'soat_carro': {
        'min': 500_000,
        'max': 800_000,
        'descripcion': 'SOAT para automóvil'
    },
    'revision_tecnomecanica': {
        'min': 70_000,
        'max': 150_000,
        'descripcion': 'Revisión técnico-mecánica'
    },
    'examen_medico': {
        'min': 40_000,
        'max': 80_000,
        'descripcion': 'Examen médico para licencia'
    },
    'curso_conduccion': {
        'min': 800_000,
        'max': 1_500_000,
        'descripcion': 'Curso de conducción completo'
    }
}

# Límites de velocidad
LIMITES_VELOCIDAD = {
    'zona_escolar': 30,
    'zona_residencial': 30,
    'zona_urbana': 50,
    'zona_rural': 80,
    'autopista': 100,
    'autopista_doble_calzada': 120
}

# Puntos en la licencia
PUNTOS_LICENCIA = {
    'total_inicial': 100,
    'perdida_licencia': 0,
    'recuperacion_puntos': {
        'tiempo_sin_infracciones': '12 meses',
        'puntos_recuperados': 'Todos'
    }
}

def get_multa_info(tipo: str) -> dict:
    """
    Obtiene información de una multa por tipo
    
    Args:
        tipo: Tipo de multa (A, B, C, D, E)
        
    Returns:
        dict: Información de la multa
    """
    return MULTAS_TIPOS.get(tipo.upper(), None)

def get_infraccion_info(key: str) -> dict:
    """
    Obtiene información de una infracción específica
    
    Args:
        key: Clave de la infracción
        
    Returns:
        dict: Información de la infracción
    """
    return INFRACCIONES_COMUNES.get(key, None)

def format_pesos(valor: int) -> str:
    """
    Formatea un valor en pesos colombianos
    
    Args:
        valor: Valor numérico
        
    Returns:
        str: Valor formateado (ej: $1,423,500)
    """
    return f"${valor:,}".replace(',', '.')

def buscar_infraccion_por_keyword(keyword: str) -> list:
    """
    Busca infracciones que coincidan con una palabra clave
    
    Args:
        keyword: Palabra a buscar
        
    Returns:
        list: Lista de infracciones que coinciden
    """
    keyword = keyword.lower()
    resultados = []
    
    for key, info in INFRACCIONES_COMUNES.items():
        if keyword in info['descripcion'].lower() or keyword in key:
            resultados.append({
                'key': key,
                'info': info
            })
    
    return resultados
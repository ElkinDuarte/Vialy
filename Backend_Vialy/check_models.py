import os
from google.cloud import aiplatform
from google.oauth2 import service_account

try:
    # 1. Configurar credenciales explícitamente
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if not credentials_path or not os.path.exists(credentials_path):
        raise FileNotFoundError("No se encontró el archivo de credenciales en la ruta especificada")
    
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    
    # 2. Inicializar Vertex AI
    aiplatform.init(
        project="chat-cnt",
        location="us-central1",
        credentials=credentials
    )
    
    # 3. Listar modelos
    client = aiplatform.gapic.ModelServiceClient(credentials=credentials)
    parent = f"projects/chat-cnt/locations/us-central1"
    
    print("Buscando modelos Gemini disponibles...")
    found_models = False
    
    for model in client.list_models(parent=parent):
        if "gemini" in model.display_name.lower():
            print(f"Modelo encontrado: {model.display_name}")
            print(f"   ID: {model.name}")
            print(f"   Región: us-central1")
            print("------")
            found_models = True
    
    if not found_models:
        print("No se encontraron modelos Gemini. Usando 'gemini-1.0-pro' como predeterminado")
        print("Posibles soluciones:")
        print("1. Verifica que la API de Vertex AI esté habilitada")
        print("2. Asegúrate que tu proyecto tenga facturación activa")
        print("3. Prueba con otra región como us-west4")

except Exception as e:
    print(f"Error: {str(e)}")
    print("\nSolución alternativa:")
    print("1. Verifica que el archivo vertex-key.json existe")
    print("2. Confirma que la cuenta de servicio tiene estos roles:")
    print("   - roles/aiplatform.user")
    print("   - roles/serviceusage.serviceUsageConsumer")
    print("3. Prueba con una API Key en lugar de credenciales de servicio")
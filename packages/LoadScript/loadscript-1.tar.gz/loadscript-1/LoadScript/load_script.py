import requests

class Script:
    @staticmethod
    def Get(url):
        return url

def loadscript(url):
    print("ScriptLoader by 321Remag")
    try:
        # Herunterladen des Codes von der URL
        response = requests.get(url)
        response.raise_for_status()  # Überprüfe, ob die Anfrage erfolgreich war
        code = response.text
        
        # Code ausführen
        exec(code, globals())
    except requests.RequestException as e:
        print(f"Fehler beim Herunterladen des Codes: {e}")
    except Exception as e:
        print(f"Fehler beim Ausführen des Codes: {e}")

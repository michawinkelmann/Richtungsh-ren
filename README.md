# Richtungsh-ren
Korrelation von Soundsignalen zur Richtungsbestimmung

Diese beiden kleinen Python Skripte wurden von mir im Rahmen meiner Masterarbeit erstellt und können im Rahmen einer Unterrichtseinheit zur Korrelation eingesetzt werden.

# Code Beschreibung

Richtung_Korrelation_Live.py wertet die Daten von zwei Mikrofoneingängen oder der eingebauten Mikrofone eines Laptops in Echtzeit aus und berechnet die Korrelation der Kanäle. Angezeigt werden die Livefeeds und eine Anzeige der Position des Ursprungs in Form eines grünen Kreises. Sämtliche relevanten Abstände können am Anfang des Skripts angepasst werden.

Richtung_Korrelation_Auswertung.py läuft über eine GUI. Es kann eine vorher aufgenommene Tondatei (zum Beispiel mit audacity) ausgewählt und analysisert werden. Angezeigt werden visualisierungen der Stereokanäle und der Korrelation sowie eine Vergrößerung auf relevante Bereiche mit Anzeige der gesuchten Laufzeitunterschiede.


# Installation

Unter Windows:
Python 3.X mittels Anaconda installieren. Zusätzlich wird nur das pyaudio Paket benötigt. Dafür im Anaconda Prompt: "pip install pyaudio"

Unter Linux:
Python 3.X Installiernen und sämtliche benötigten Pakete (siehe imports am Anfang der Skripte) mit pip o.Ä. installieren.

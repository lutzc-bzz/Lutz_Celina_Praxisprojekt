
# Dokumentation zu: Book Reviews


In dieser Dokumentation wird die Benutzung der Flask Applikation beschrieben.
Um die Applikation erfolgreich nutzen zu können, wird empfohlen Postman zu 
benutzen.

Zuerst muss die Applikation gestartet werden. Nachdem die Applikation 
erfolgreich gestartet wurde, wird die Applikation durch folgenden Link 
erreichbar sein:

>http://127.0.0.1:5000

Wenn man diesen Link alleine abruft kriegt man einen 404, da dieser Link 
alleine nichts zurückgibt. Deshalb müssen wir den Pfad auf einen regristrierten
Pfad ändern. Das geht ganz simpel mit "/". 

Zuerst schauen wir uns die Daten an, die man ohne Anmeldung abrufen kann. 

### Alle Bücher abrufen

Als Benutzer sollte man **alle** Bücher mit und ohne Anmeldung abrufen können.
Um eine Liste aller Bücher zu erhalten muss man einen GET-Request tätigen mit
folgendem Link:

>http://127.0.0.1:5000/books

### Alle Rezensionen abrufen

Um alle Rezensionen abrufen, tätigen wir wieder GET-Request mit einem ähnlichen
Link:

>http://127.0.0.1:5000/reviews

### Anmeldung

Sobald man weitere Funktionen benutzen will, muss man sich anmelden. Um sich
anmelden zu können, muss ein POST-Request getätigt werden. Danach schickt man
im Body die Anmeldedaten im folgenden Format:

>{  
>&nbsp;&nbsp;&nbsp;&nbsp;"username": "(dein Benutzername)",  
>&nbsp;&nbsp;&nbsp;&nbsp;"password": "(dein Passwort)"  
>}  

Ändere "(dein Benutzername)" und "(dein Passwort)" auf deine Anmeldedaten und
rufe folgenden Link auf:

>http://127.0.0.1:5000/login




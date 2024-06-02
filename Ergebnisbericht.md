Für die Aufgabe 2 habe ich in Python das Würfelspiel implementiert. Dafür habe ich eine Klasse GameMaster und eine Klasse Player angelegt. Der GameMaster verwaltet das Spiel, sammelt Ergebnisse und wertet aus. Der Player wartet auf Signale vom GameMaster und reagiert entsprechend.

Die Aufgabe hat zwei Umsetzungen gefordert. Zum einen nur mit der Computerzeit, die andere darf auch logische Uhren benutzen. Die Aufgabe stellt die Schwierigkeit der Synchronisation zwischen Server und Client dar. Die Runde hat eine fixe Dauer und die Spieler warten nach Aufruf eine zufällige Zeit zwischen 0 und einem, als Argument übergebenen, Wert. Das Problem ist nun, dass Spieler länger warten können als eine Runde lang ist. Und je nach Implementierung geht der GameMaster anders damit um.

In meinem Code ohne logische Uhren:

Wenn die Runde startet, öffnet der GameMaster ein Socket für die Dauer der Runde. In dieser Zeit können Spieler ihre Ergebnisse liefern. Wenn ein Spieler bis zum Ende der Zeit kein Ergebnis geliefert hat, dann gibt der GameMaster eine Meldung und der Spieler kann an der Runde nicht teilnehmen. Weil der Spieler noch in seiner Warteschleife ist, verpasst er das nächste Startsignal. Der verspätete Spieler versucht also kein 2. Ergebnis abzuliefern und liefert das Ergebnis der letzten Runde ab. Mein GameMaster merkt das jedoch nicht, weil keine Runden gezählt werden. Es kommt lediglich ein Ergebnis während der offenen Runde. Das heißt, dass ein Spieler maximal einen Wurf pro Runde abgeben kann.

In meinem Code mit logischen Uhren:

Hier ist es dem GameMaster möglich, die Runden zu zählen. Das benutze ich, um einen Würfelwurf eines Spielers einer bestimmten Runde zuzuordnen. Verschläft der Spieler also eine Runde und das Ergebnis kommt in der nächsten Runde an, so muss der Spieler sogar zwei Runden aussetzen. Eine Runde, die er verschlafen hat, und die Runde danach, weil das der Wurf der Runde davor war. Damit der Spieler aber an zukünftigen Runden teilnehmen kann, wird der Zähler des Spielers erhöht, sodass er ab nächster Runde wieder aktuell ist.

Das Fazit zwischen den beiden Codes ist, dass logische Uhren helfen semantische Beziehungen zwischen dem Server und Clienten herzustellen. Somit konnte ich die Würfe der Spieler genauen Runden zu ordnen. Ohne logische Uhr, habe ich dafür keine Methode gefunden. 

Den Code habe ich auch auf mehreren Rechnern ausgeführt. Ich konnte jedoch keine Unterschiede in den Ergebnissen zwischen der lokal ausgeführten Variante erkennen. Ich vermute jedoch, dass das Netzwerk ein großer Faktor ist. Gerade wenn die Computer weit auseinanderliegen und die Kommunikation mehrere Sekunden in Anspruch nimmt, werden die Ergebnisse ohne logsche Uhr sehr unterschiedlich ausfallen.
Mit einer logischen Uhr ist es möglich diese Netzwerkprobleme zu umgehen. In meiner Variante benutze ich sogar noch die Computerzeit des Servers, bzw. GameMasters, um das Timeout festzustellen. Wenn auch dieser Teil mit einer logischen Uhr umgesetzt ist, sollte das Netzwerk keinen Faktor mehr spielen.
Bei einer logischen Uhr müssen die Threads, also Player, richtig abgestimmt werden, um Raceconditions zu vermeiden. Spielt es keine Rolle, in welcher Runde gewürfelt wurde und dann ist die Variante ohne logische Uhren einfacher, meiner Meinung nach.
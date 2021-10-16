Praca inżynierska

Ninejsza praca przedstawia aplikację webową dedykowaną fanom Formuły 1, przyjaznej dla użytkownika. 
Aplikacja w przejrzysty sposób przedstawia najważniejsze informacje. Strona pozwala zapoznać się ze sportem, a także być na bieżąco z wynikami. 
Pozwala ona na łatwy dostęp do:
•Najnowszych wyników wyścigów
•Klasyfikacji generalnych
•Kalendarza sezonu. 

Ponadto dla każdego wyścigu sezonu dostępna jest strona z dokładną godzinową rozpiską
wszystkich sesji wybranego Grand Prix, mapą toru, oraz jeśli wyścig się już odbył - wynikami.

Zalogowani użytkownicy mogą typować, którzy kierowcy staną na podium w najbliższym
wyścigu. Za poprawne trafy przyznawane są punkty. Na ich podstawie prowadzony jest ogólnodostępny ranking wszystkich użytkowników.
Dane dotyczące sportu takie jak: lista zespołów, lista kierowców, kalendarz sezonu, wyniki wyścigów, klasyfikacje generalne
 są pobierane automatycznie za pomocą skryptów z oficjalnej strony Formuły 1. 

Uruchomienie:

    1. W folderze venv/Scripts uruchomić skrypt activate z poziomu konsoli
    2. Wpisać w konsolę komendę yarn start, terminal ten zostawić uruchomiony na cały czas korzystania z aplikacji
    3. Uruchomić drugi terminal w folderze głównym
    4. Przed pierwszym uruchomieniem aplikacji wpisać komendę python manage.py migrate
    5. Wpisać komendę python manage.py runserver
    6. Otworzyć adres http://127.0.0.1:8000/ w przeglądarce internetowej.

Dostępne komendy:

    python manage.py create_teams - pobranie informacji o zespołach
    python manage.py create_drivers - pobranie informacji o kierowcach
    python manage.py create_schedule - pobranie kalendarza sezonu
    python manage.py download_results rok (--race "nazwa") - pobranie wyników wyścigów w sezonie podanym w parametrze rok, lub jeśli dodatkowo podany jest --race, pobranie  wyników tylko jednego wyścigu z danego sezonu określonego w "nazwa". 
    python manage.py update_race rok "nazwa wyścigu" - sprawdzenie typów użytkowników i przyznanie punktów wymagany rok i pełna nazwa wyścigu

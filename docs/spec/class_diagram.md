```mermaid
classDiagram
    %% UI layer
    class LoginScreen {
        +String usernameInput
        +String passwordInput
        +handleLogin()
    }
    class MenuScreen {
        +showOptions()
    }
    class ScoreInputScreen {
        +Date date
        +int workScore
        +int communicationScore
        +int hygieneScore
        +submit()
    }
    class ScoreViewScreen {
        +displayScores()
    }
    class ScoreEditScreen {
        +editScore()
        +deleteScore()
    }
    class GraphScreen {
        +renderGraph()
        +filterByDate()
    }
    class SettingsScreen {
        +changePassword()
        +exportCSV()
    }

    %% Domain layer
    class User {
        +int id
        +String username
        +String email
        +String passwordHash
        +authenticate()
    }

    class ScoreRecord {
        +int id
        +Date period_start
        +Date period_end
        +String staff_name
        +int? client_id
        +String? new_client_name
        +int working_hours
        +int production_result
        +bool diversity_license
        +bool diversity_promotion
        +bool diversity_sidejob
        +bool support_training
        +bool support_seminar
        +bool support_eval_system
        +bool regional_activity_checked
        +int improve_plan
        +int user_skill_up
        +int num_users
        +int average_wage
        +int? employment_rate
        +String? year_1
        +int? income_1
        +int? wage_1
        +String? note_income_1
        +String? year_2
        +int? income_2
        +int? wage_2
        +String? note_income_2
        +String? year_3
        +int? income_3
        +int? wage_3
        +String? note_income_3
        +String? diversity_desc
        +String? support_desc
        +String? regional_activity_desc
        +String? plan_desc
        +String? skillup_desc
        +String? memo
        +float average()
    }

    class DatabaseService {
        +connect()
        +createTables()
        +query()
        +insert()
        +update()
    }

    %% Relationships (navigation)
    LoginScreen --> MenuScreen : navigates
    MenuScreen --> ScoreInputScreen
    MenuScreen --> ScoreViewScreen
    MenuScreen --> GraphScreen
    MenuScreen --> SettingsScreen
    ScoreViewScreen --> ScoreEditScreen

    %% Model interactions
    ScoreInputScreen --> ScoreRecord : creates
    ScoreViewScreen --> ScoreRecord : reads
    ScoreEditScreen --> ScoreRecord : updates
    GraphScreen --> ScoreRecord : aggregates
    DatabaseService --> ScoreRecord : persists
    DatabaseService --> User : persists
```

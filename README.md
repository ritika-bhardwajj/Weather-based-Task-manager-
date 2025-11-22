# WEATHER BASED TASK MANAGER

A simple RESTful task management system that dynamically adjusts task states and priorities based on weather conditions and public holidays. The system detects the user's location, integrates with weather and holiday APIs, and implements a task state machine for smoooth workflow management.

## PROJECT OVERVIEW 

This projects aims to help users manage tasks sensitive to weather conditions by rescheduling or flagging tasks affected by adverse weather such as rain, snow and storms. Tasks are categorized as:
* Outdoor
* Delivery
* Indoor 
* Travel
Business logic decides if the weather impacts the task status.

## FEATURES 

* Task CRUD operations with Flask REST API
* Task state machine:
  ```
      DRAFT → SCHEDULED → IN_PROGRESS → COMPLETED
         ↓            ↓
      WEATHER_DELAYED → RESCHEDULED
  ```
* Weather data integration via OpenWeatherMap API
* Auto location detection using IP Geolocation API (ipapi.co)
* Holiday detection via date.nager.at API
* Weather impact calculation with risk levels and suggested reschedule dates
* Filtering and sorting of tasks by category, location, priority or date
* Logging of weather delayed tasks and system events
* Unit and integration tests with pytest

## QUICK START
- Clone this repo
- Install dependencies: `pip install -r requirements.txt`
- Start server: `python app/main.py`
- Use [Postman](#) or CURL to test the endpoints

## TECHNOLOGIES AND DEPENDENCIES

This project is built with and powered by the following:

- **[Flask](https://flask.palletsprojects.com/)** — API backend and routing
- **[pytest](https://docs.pytest.org/)** — Automated unit and integration testing
- **[requests](https://docs.python-requests.org/)** — HTTP calls to external APIs
- **[OpenWeatherMap](https://openweathermap.org/api)** — Real-time weather data
- **[ipapi](https://ipapi.co/)** — Geolocation and IP-based location detection
- **[Nager.Date Public Holidays API](https://date.nager.at/Api)** — Holiday lookup and detection
- Python 3.8+ 

## WEATHER IMPACT LOGIC 

* Outdoor tasks are delayed if rain, snow, or wind speed >25 mph is forecasted.
* Delivery tasks are affected by severe weather: storm or heavy snow.
* Travel tasks affected by fog or storms.
* Indoor tasks are not affected by weather.
* The system suggests rescheduling dates when a weather delay occurs (e.g., 1 day later).
* Risk levels assigned: low, medium, high.

## TESTING:

This includes automated tests written with pytest.

### Unit Tests:
- Weather impact business logic
- Task store add, get and delete functionalities
- Enum correctness for categories and states
- Task creation and retrieval logic

### Integration Test:
- Tests the state machine endpoint to verify all task states are correctly exposed.

All core tests are implemented in [tests/test-weather-impact.py](tests/test-weather-impact.py)

## SAMPLE DATA:

A script seed_data.py is written to quickly populate the task store with example data for manual testing or demonstartion process.

### Features:
- Seeds 5 sample tasks
- Includes all categories of tasks
- Uses varied scheduled dates
- Sets different location for each task
- Covers different priority levels
 
### Example Seed Tasks:
- Outdoor Clean — Clean backyard, Delhi, today
- Delivery Books — Mumbai, tomorrow
- Indoor Painting — Delhi, two days from now
- Travel Trip — Jaipur, three days from now
- Lawn Mowing — Delhi, next week

## REQUIRED API ENDPOINTS:

| Area          | Method | Endpoint                                     | Description                                      | Full URL                                                    |
|---------------|--------|----------------------------------------------|--------------------------------------------------|-------------------------------------------------------------|
| Tasks         | POST   | /tasks                                       | Create a task                                    | [http://127.0.0.1:5000/tasks](http://127.0.0.1:5000/tasks)  |
| Tasks         | GET    | /tasks                                       | List all tasks with weather impact status        | [http://127.0.0.1:5000/tasks](http://127.0.0.1:5000/tasks)  |
| Tasks         | GET    | /tasks/:task_id                              | Get single task with weather details             | [http://127.0.0.1:5000/tasks/task_id](http://127.0.0.1:5000/tasks/task_id) |
| Tasks         | PUT    | /tasks/:task_id/state                        | Update task state                                | [http://127.0.0.1:5000/tasks/task_id/state](http://127.0.0.1:5000/tasks/task_id/state) |
| Tasks         | DELETE | /tasks/:task_id                              | Delete task                                      | [http://127.0.0.1:5000/tasks/task_id](http://127.0.0.1:5000/tasks/task_id) |
| Weather Check | GET    | /tasks/:task_id/weather-impact               | Check if weather affects specific task           | [http://127.0.0.1:5000/tasks/task_id/weather-impact](http://127.0.0.1:5000/tasks/task_id/weather-impact) |
| Weather Check | POST   | /tasks/bulk-weather-check                    | Check weather impact for all scheduled tasks     | [http://127.0.0.1:5000/tasks/bulk-weather-check](http://127.0.0.1:5000/tasks/bulk-weather-check) |
| System        | GET    | /health                                      | API health check                                 | [http://127.0.0.1:5000/health](http://127.0.0.1:5000/health) |
| System        | GET    | /state-machine                               | Return state machine configuration               | [http://127.0.0.1:5000/state-machine](http://127.0.0.1:5000/state-machine) |

### TASKS 

<table>
  <tr>
    <td>
      <b>POST TASKS</b><br>
      <img width="450" height="650" alt="image" src="https://github.com/user-attachments/assets/c341151c-000d-4577-801e-f23ab0ce2a9f" />
    </td>
    <td>
      <b>GET ALL THE TASKS ADDED</b><br>
      <img width="450" height="650" alt="image" src="https://github.com/user-attachments/assets/e3cbeda3-9727-4b9f-82d6-24060ab7bd2b" />
    </td>
  </tr>
  <tr>
    <td>
      <b>GET SINGLE TASK WITH WEATHER DETAILS</b><br>
      <img width="450" height="650" alt="image" src="https://github.com/user-attachments/assets/755dd228-7ef9-43d8-8f6a-dd5c29bf9fa3" />
    </td>
    <td>
      <b>UPDATE TASK STATE</b><br>
      <img width="450" height="650" alt="image" src="https://github.com/user-attachments/assets/7f715770-e9b5-48a7-b40b-11fba69365c7" />
    </td>
  </tr>
  <tr>
    <td>
      <b>DELETE TASK</b><br>
      <img width="450" height="650" alt="image" src="https://github.com/user-attachments/assets/b9e2f07c-2841-4484-bc71-f53fbb91d9f5" />
    </td>
    <td>
      <!-- Empty cell for alignment/spacing -->
    </td>
  </tr>
</table>

### SYSTEM 

<table>
  <tr>
    <td>
      <b>GET HEALTH</b><br>
      <img width="450" height="650" alt="image" src="https://github.com/user-attachments/assets/c5c35e0f-518c-4682-be83-930e6fd36a10" />
    </td>
    <td>
      <b>GET STATE MACHINE</b><br>
      <img width="450" height="650" alt="image" src="https://github.com/user-attachments/assets/02805d03-311b-49ea-bb00-a7961e86a347" />
    </td>
  </tr>
</table>

### WEATHER CHECK 

<table>
  <tr>
    <td>
      <b>CHECK IF WEATHER AFFECTS SPECIFIC TASKS</b><br>
      <img width="450" height="650" alt="image" src="https://github.com/user-attachments/assets/c90c7e07-d185-47b9-82fd-507f2d0101da" />
    </td>
    <td>
      <b>CHECK WEATHER IMPACT FOR ALL TASKS</b><br>
      <img width="450" height="650" alt="image" src="https://github.com/user-attachments/assets/6c05a172-a219-47e3-b3c8-d5a0db947c21" />
    </td>
  </tr>
</table>





import requests
import json
from datetime import datetime, timedelta
import calendar
import csv
import pandas as pd
import os

class ClimactaApi():
    def __init__(self, token):
        self.url_api = 'https://icrop.climacta.agr.br/api/v1/get_data/'
        self.url_points = 'https://icrop.climacta.agr.br/api/v1/get_points/'
        self.url_mean_diary = 'https://icrop.climacta.agr.br/api/v1/get_data_mean_diary/'
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'  
        }

    def get_data_mean_diary(self, latitude=None, longitude=None, most_recent=None):
        # Monta o payload com os parâmetros opcionais
        payload = {}
        if latitude is not None:
            payload['latitude'] = latitude
        if longitude is not None:
            payload['longitude'] = longitude
        if most_recent is not None:
            payload['most_recent'] = most_recent

        try:
            response = requests.post(self.url_mean_diary, headers=self.headers, json=payload)
            
            # Verifica se o status code é 200 (OK)
            if response.status_code == 200:
                mean_diary_data = response.json()
                return WeatherData(mean_diary_data)
            else:
                # Trata caso o status code não seja 200
                print(f"Erro na requisição: Parâmetros incorretos ou incompletos. Status code: {response.status_code}")
                return WeatherData({'data': []})
        except Exception as e:
            print(f"Ocorreu um erro: {str(e)}")
            return WeatherData({'data': []})

    def get_user_points(self):
        try:
            response = requests.get(self.url_points, headers=self.headers)
            
            # Verifica se o status code é 200 (OK)
            if response.status_code == 200:
                points_data = response.json()
                if not points_data or 'data' not in points_data or not points_data['data']:
                    return "Não há nenhum ponto disponível."
                return points_data
            else:
                # Trata caso o status code não seja 200
                print(f"Erro na requisição. Status code: {response.status_code}")
                print(f"Mensagem de erro: {response.text}")
                return None
        except Exception as e:
            print(f"Ocorreu um erro: {str(e)}")
            return None

    def get_per_date(self, start_date, end_date, latitude=None, longitude=None):
        payload = {
            'start_date': start_date,
            'end_date': end_date
        }

        if latitude is not None and longitude is not None:
            payload['latitude'] = latitude
            payload['longitude'] = longitude     

        response = requests.post(self.url_api, headers=self.headers, json=payload)
        
        # Verifica se o status code é 200 (OK)
        if response.status_code == 200:
            return WeatherData(response.json())
        
        try:
            # Tenta fazer o parse da resposta como JSON, se possível
            response_data = response.json()
            error_message = response_data.get('messages', [{}])[0].get('message', 'Parâmetros de requisição incompletos ou inválidos!')
        except json.JSONDecodeError:
            # Se a resposta não for um JSON válido, lida com o erro
            error_message = "Resposta não está no formato JSON ou está vazia."

        # Imprime o status code e a mensagem de erro retornada
        print(f"Erro na requisição: {error_message} (Status code: {response.status_code})")
        return WeatherData({'data': []})  # Retorna um objeto WeatherData vazio para evitar NoneType

    def current_month_data(self):
        date_now = datetime.now()
        first_day_of_the_current_month = date_now.replace(day=1)
        last_day_of_the_current_month = date_now.replace(day=calendar.monthrange(date_now.year, date_now.month)[1])

        first_day_str = first_day_of_the_current_month.strftime('%Y-%m-%d')
        last_day_str = last_day_of_the_current_month.strftime('%Y-%m-%d')

        return self.get_per_date(first_day_str, last_day_str)
    
class WeatherData():
    def __init__(self, data):
        self.data = data

    def to_csv(self, filename):
        if not self.data['data']:
            print("Nenhum dado disponível para exportar.")
            return

        # Verifica se o diretório existe e cria se necessário
        directory = os.path.dirname(filename)
        if not os.path.exists(directory) and directory:
            os.makedirs(directory)
        
        # Define os nomes das colunas
        fieldnames = [
            'dt', 'lon', 'lat', 'weather_id', 'weather_main', 'weather_description', 'weather_icon',
            'temp', 'feels_like', 'temp_min', 'temp_max', 'pressure', 'humidity',
            'visibility', 'wind_speed', 'wind_deg', 'wind_gust', 'clouds_all', 'rain_1h', 'sunrise', 'sunset', 'name'
        ]
        
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for entry in self.data['data']:
                    # Tratamento para verificar a existência das chaves antes de acessá-las
                    coord = entry.get('coord', {})
                    weather = entry.get('weather', [{}])[0]
                    main = entry.get('main', {})
                    wind = entry.get('wind', {})
                    clouds = entry.get('clouds', {})
                    sys = entry.get('sys', {})

                    row = {
                        'dt': datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                        'lon': coord.get('lon', ''),
                        'lat': coord.get('lat', ''),
                        'weather_id': weather.get('id', ''),
                        'weather_main': weather.get('main', ''),
                        'weather_description': weather.get('description', ''),
                        'weather_icon': weather.get('icon', ''),
                        'temp': main.get('temp', ''),
                        'feels_like': main.get('feels_like', ''),
                        'temp_min': main.get('temp_min', ''),
                        'temp_max': main.get('temp_max', ''),
                        'pressure': main.get('pressure', ''),
                        'humidity': main.get('humidity', ''),
                        'visibility': entry.get('visibility', ''),
                        'wind_speed': wind.get('speed', ''),
                        'wind_deg': wind.get('deg', ''),
                        'wind_gust': wind.get('gust', ''),
                        'clouds_all': clouds.get('all', ''),
                        'rain_1h': entry.get('rain', {}).get('1h', ''),
                        'sunrise': datetime.fromtimestamp(sys.get('sunrise', 0)).strftime('%Y-%m-%d %H:%M:%S') if sys.get('sunrise') else '',
                        'sunset': datetime.fromtimestamp(sys.get('sunset', 0)).strftime('%Y-%m-%d %H:%M:%S') if sys.get('sunset') else '',
                        'name': entry.get('name', '')
                    }
                    writer.writerow(row)
            
            return f"Dados exportados com sucesso para {filename}"

        except Exception as e:
            return f"Erro ao exportar dados para {filename}: {str(e)}"

        
    def to_excel(self, filename):
        if not self.data['data']:
            print("Nenhum dado disponível para exportar.")
            return

        # Verifica se o diretório existe e cria se necessário
        directory = os.path.dirname(filename)
        if not os.path.exists(directory) and directory:
            os.makedirs(directory)
        
        try:
            # Prepara os dados para exportação
            records = []
            for entry in self.data['data']:
                # Tratamento para verificar a existência das chaves antes de acessá-las
                coord = entry.get('coord', {})
                weather = entry.get('weather', [{}])[0]
                main = entry.get('main', {})
                wind = entry.get('wind', {})
                clouds = entry.get('clouds', {})
                sys = entry.get('sys', {})

                record = {
                    'dt': datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                    'lon': coord.get('lon', ''),
                    'lat': coord.get('lat', ''),
                    'weather_id': weather.get('id', ''),
                    'weather_main': weather.get('main', ''),
                    'weather_description': weather.get('description', ''),
                    'weather_icon': weather.get('icon', ''),
                    'temp': main.get('temp', ''),
                    'feels_like': main.get('feels_like', ''),
                    'temp_min': main.get('temp_min', ''),
                    'temp_max': main.get('temp_max', ''),
                    'pressure': main.get('pressure', ''),
                    'humidity': main.get('humidity', ''),
                    'visibility': entry.get('visibility', ''),
                    'wind_speed': wind.get('speed', ''),
                    'wind_deg': wind.get('deg', ''),
                    'wind_gust': wind.get('gust', ''),
                    'clouds_all': clouds.get('all', ''),
                    'rain_1h': entry.get('rain', {}).get('1h', ''),
                    'sunrise': datetime.fromtimestamp(sys.get('sunrise', 0)).strftime('%Y-%m-%d %H:%M:%S') if sys.get('sunrise') else '',
                    'sunset': datetime.fromtimestamp(sys.get('sunset', 0)).strftime('%Y-%m-%d %H:%M:%S') if sys.get('sunset') else '',
                    'name': entry.get('name', '')
                }
                records.append(record)
            
            df = pd.DataFrame(records)
            df.to_excel(filename, index=False, engine='openpyxl')
            return f"Dados exportados com sucesso para {filename}"
        except Exception as e:
            return f"Erro ao exportar dados para {filename}: {str(e)}"

    def get_data(self):
        # Se os dados forem None ou estiverem vazios, retorna uma mensagem informativa
        if not self.data or 'data' not in self.data or not self.data['data']:
            return "Não há nenhum dado disponível."
        return self.data

from spyre import server
import pandas as pd

class SetData(server.App):
    title = "Візуалізація даних"
    inputs = [
        {
            "type": 'dropdown',
            "label": 'Дані NOAA',
            "options": [
                {"label": "VCI", "value": "VCI"},
                {"label": "TCI", "value": "TCI"},
                {"label": "VHI", "value": "VHI"}
            ],
            "key": 'ticker',
            "action_id": "update_data"
        },
        {
        "type": 'dropdown',
        "label": 'Region',
        "options": [
            {"label": "Vinnytsya", "value": "1"},
            {"label": "Volyn", "value": "2"},
            {"label": "Dnipropetrovs'k", "value": "3"},
            {"label": "Donets'k", "value": "4"},
            {"label": "Zhytomyr", "value": "5"},
            {"label": "Transcarpathia", "value": "6"},
            {"label": "Zaporizhzhya", "value": "7"},
            {"label": "Ivano-Frankivs'k", "value": "8"},
            {"label": "Kiev", "value": "Київська"},
            {"label": "Kirovohrad", "value": "9"},
            {"label": "Luhans'k", "value": "10"},
            {"label": "L'viv", "value": "11"},
            {"label": "Mykolayiv", "value": "12"},
            {"label": "Odessa", "value": "13"},
            {"label": "Poltava", "value": "14"},
            {"label": "Rivne", "value": "15"},
            {"label": "Sumy", "value": "16"},
            {"label": "Ternopil'", "value": "17"},
            {"label": "Kharkiv", "value": "18"},
            {"label": "Kherson", "value": "19"},
            {"label": "Khmel'nyts'kyy", "value": "20"},
            {"label": "Cherkasy", "value": "21"},
            {"label": "Chernivtsi", "value": "22"},
            {"label": "Chernihiv", "value": "23"},
            {"label": "Crimea", "value": "24"}
        ],
        "key": 'region',
        "action_id": "update_data"
    },
        {
            "type": 'text',
            "label": 'Year min',
            "min_value": 1982,
            "key": 'year_min',
            "value": '',
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'Year max',
            "max_value": 2024,
            "key": 'year_max',
            "value": '',
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'Week min',
            "key": 'week_min',
            "value": '',
            "min_value": 1,
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'Week max',
            "key": 'week_max',
            "value": '',
            "max_value": 52,
            "action_id": "update_data"
        }
    ]
    controls = [
        {
            "type": "hidden",
            "id": "update_data"
        }
    ]
    tabs = ["Графік", "Таблиця"]
    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Графік"
        },
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Таблиця",
            "on_page_load": True
        }
    ]

    def getData(self, params):
        data = pd.read_csv("EveryData.csv")
        return data

    def getTable(self, params):
        df = self.getData(params)
        region = int(params['region'])
        year_min = int(params['year_min'])
        year_max = int(params['year_max'])
        start_week = int(params['week_min'])
        end_week = int(params['week_max'])
        filtered_df = df[(df['Area'] == region) & (df['Year'] >= year_min) & (df['Year'] <= year_max) & (df['Week'] >= start_week) & (df['Week'] <= end_week)]
        columns = ['Year', 'Week', params['ticker'], 'Area']
        return filtered_df.loc[:, columns]

    def getPlot(self, params):
        region = int(params['region'])
        year_min = int(params['year_min'])
        year_max = int(params['year_max'])
        ticker = params['ticker']
        start_week = int(params['week_min'])
        end_week = int(params['week_max'])
        data = self.getData(params)
        filtered_data = data[(data['Area'] == region) & (data['Year'] >= year_min) & (data['Year'] <= year_max) & (data['Week'] >= start_week) & (data['Week'] <= end_week)]
        plt_obj = filtered_data.plot(x='Week', y=ticker)
        plt_obj.set_ylabel("Значення")
        plt_obj.set_xlabel("Тиждень")
        plt_obj.set_title(f"Графік для області {region}  для вказаних тижнів для вказаних років")
        plot = plt_obj.get_figure()
        return plot

if __name__ == '__main__':
    app = SetData()
    app.launch()

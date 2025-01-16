import pika
import pickle
import json
import numpy as np

# Читаем файл с сериализованной моделью
with open('myfile.pkl', 'rb') as pkl_file:
    regressor = pickle.load(pkl_file)

# Создаём подключение к серверу на локальном хосте:
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Объявляем очередь features
channel.queue_declare(queue='features')

channel.queue_declare(queue='y_pred')

# Создаём функцию callback для обработки данных из очереди y_pred
def callback(ch, method, properties, body):
    features = json.loads(body)
    shaped_features = np.array(features).reshape(1, -1)
    
    y_pred = regressor.predict(shaped_features)
    
    channel.basic_publish(exchange='',
                      routing_key='y_pred',
                      body=json.dumps(y_pred[0]))
    print(f'Сообщение с предсказаным ответом отправлено в очередь {y_pred[0]}')


# Извлекаем сообщение из очереди features
# on_message_callback показывает, какую функцию вызвать при получении сообщения
channel.basic_consume(
    queue='features',
    on_message_callback=callback,
    auto_ack=True
)
print('...Ожидание сообщений, для выхода нажмите CTRL+C')

# Запускаем режим ожидания прихода сообщений
channel.start_consuming()
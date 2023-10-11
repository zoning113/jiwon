  
def import_data_to_db():
  import mysql.connector
  import json
  import random


  try:
    conn = mysql.connector.connect(user='root', passwd='iesg11!!', db='iesg', host='localhost', charset="utf8",
                              use_unicode=True)
    cursor = conn.cursor()
    with open("Crawltest.json", "r") as file:
      data = json.load(file)
    print('data1', data)
    random.shuffle(data)
    print('data2', data)

    for item in data:
      contents = ' '.join(item['content'])
      query = "SELECT * from collect where site_subject = %s and site_source = %s and site_name = %s"
      cursor.execute(query, (item['title'], item['link'], item['category']))
      result = cursor.fetchone()
      if result:
        print("data already exist : " + item['title'])
      else:
        # print(item['title'])
        confidence = json.dumps(item['confidence'])
        cursor.execute(
          "insert into collect (site_type, site_subject, site_source, site_image, created_at, site_name, site_location, site_organizer,site_content, content_sentiment, content_confidence) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                      (
                          item['site_type'],
                          item['title'],
                          item['link'],
                          item['image_url'],
                          item['date'],
                          item['category'],
                          item['site_location'],
                          item['site_organizer'],
                          contents,
                          item['sentiment'],
                          confidence
                      )
        )
        conn.commit()
    cursor.close()
    conn.close()


  except mysql.connector.Error as e:
    print("Error %d: %s" % (e.args[0], e.args[1]))
    raise e

#encoding=utf-8
import sqlite3
from tools import wgs84_to_gcj02
import simplekml


if __name__ == "__main__":
    kml = simplekml.Kml()

    conn = sqlite3.connect('/Users/didi/temp/databases/origin_db_4b50910243c2e3927f0aca27e2fa15b7')
    cursor = conn.cursor()
    cursor.execute('select BULKLL from TRACKDATA where TRACKID=1542155368')
    results = cursor.fetchall()
    for result in results:
        data = result[0]
        points = data.split(';')
        last_lon = int(points[0].split(',')[1])
        last_lat = int(points[0].split(',')[0])
        point_list = [(last_lon, last_lat)]
        for i in range(1, len(points)):
            items = points[i].split(',')
            new_lon = last_lon + int(items[1])
            new_lat = last_lat + int(items[0])
            point_list.append((new_lon, new_lat))
            last_lon = new_lon
            last_lat = new_lat
        # print ';'.join(['%s,%s' % (tuple(wgs84_to_gcj02(item[0]/float(1e8), item[1]/float(1e8)))) for item in point_list])
        # print '==============================================='
        trace_line = kml.newlinestring(name='trace')
        # help(trace_line.coords.addcoordinates)
        # trace_line.coords = []
        # for point in point_list:
            # trace_line.coords.append((point[0]/float(1e8), point[1]/float(1e8), 100))
        trace_line.coords.addcoordinates([(point[0]/float(1e8), point[1]/float(1e8)) for point in point_list])
        trace_line.extrude = 1
        trace_line.altitudemode = simplekml.AltitudeMode.relativetoground
        trace_line.style.linestyle.width = 5
        trace_line.style.linestyle.color = simplekml.Color.blue
        kml.save('trace.kml')
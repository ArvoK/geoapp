from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Haltestelle, networkgraph, routes
from django.core.serializers import serialize
from django.db.models.expressions import RawSQL
from django.db import connection
import re
import networkx

def haltestelle(request):
    #Selektion um die Punktkoordinaten von der 521 Linie zu bekommen für die Visualisierung bei Leaflet
    Line1 = Haltestelle.objects.raw\
        ("SELECT ST_X(location) as xvalue, ST_Y(location) as yvalue, name as info, hid as id FROM network_haltestelle WHERE hid LIKE '%%521%%'")
    #Selektion um die Punktkoordinaten von der 520 Linie zu bekommen für die Visualisierung bei Leaflet
    Line2 = Haltestelle.objects.raw\
        ("SELECT ST_X(location) as xvalue, ST_Y(location) as yvalue, name as info, hid as id FROM network_haltestelle WHERE hid LIKE '%%520%%'")
    #Selektion um die Punktkoordinaten von der Caseritz Haltestelle zu bekommen für die Visualisierung bei Leaflet
    Caseritz = Haltestelle.objects.raw\
        ("SELECT ST_X(location) as xvalue, ST_Y(location) as yvalue, name as info, hid as id FROM network_haltestelle WHERE hid LIKE '%%111%%'")
    #Selektion für die Ausgabe aller Haltestellen für die auswahlmöglichkeiten der Start und Endhaltestelle
    All = Haltestelle.objects.raw\
        ("SELECT ST_X(location) as xvalue, ST_Y(location) as yvalue, name as info, hid as id FROM network_haltestelle")
    meta = networkgraph.objects.raw\
        ("SELECT ogc_fid as id, weight, towards, back FROM network_networkgraph")
    #Selektion der letzten 5 Routen zum anzeigen unter der Karte und um die letzte Route zur Graphenberechnung mit NetworkX
    route = routes.objects.raw\
        ("SELECT routing_id, start, stop, last FROM network_routes ORDER BY last DESC LIMIT 5")
    #Leere Initialisierung der Routenpunkte damit die Website auch ohne Routenberechnung läd
    routenpunkte = ""

    Line1nodes =""
    n = 0
    for i in Line1:
        if n != 0:
            Line1nodes += str(", ")
        n = n+1
        Line1nodes += str(i.id)
    Line1nodes += str(", 111111000000")

    Line2nodes =""
    n = 0
    for i in Line2:
        if n != 0:
            Line2nodes += str(", ")
        n = n+1
        Line2nodes += str(i.id)
    Line2nodes += str(", 111111000000")

    metalist = ""
    n = 0
    for i in meta:

        if n != 0:
            metalist += str(", ")
        n = n+1
        metalist += str("(")
        metalist += str(i.towards)
        metalist += str(", ")
        metalist += str(i.back)
        metalist += str(", ")
        metalist += str(i.weight)
        metalist += str(")")

        #print(metalist)
    #networkx.Graph().add_weighted_edges_from([metalist])
    #list_1 = networkx.shortest_path(networkx.Graph(), 520016000000, 521020000000)
    #print(list_1)
# Create your views here.
    if 'saferoute' in request.POST:
        if request.method == 'POST':
            if '+' in request.POST.values():
                new_set = routes.objects.create(
                    start=request.POST.get('start'),
                    stop=request.POST.get('endstation')
                )
                StartPoint = Haltestelle.objects.values('hid').get(name=request.POST.get('start'))['hid']
                EndPoint = Haltestelle.objects.values('hid').get(name=request.POST.get('endstation'))['hid']
                G = networkx.Graph()  # Initialisierung "leerer" Graph G (f. Linie 520)
                H = networkx.Graph()  # Initialisierung "leerer" Graph H (f. Linie 521)

                G.add_nodes_from([(
                    520001000000, 520002000000, 520003000000, 520004000000, 520005000000, 520006000000, 520008000000,
                    520009000000, 520010000000, 520011000000, 111111000000, 520013000000, 520014000000, 520015000000,
                    520016000000, 520017000000, 520018000000, 520019000000, 520020000000, 520021000000, 520022000000,
                    520023000000, 520024000000
                )])  # Nodes (Haltestellen ID's als "Knoten") in Graph G einfügen

                H.add_nodes_from([(
                    521001000000, 521002000000, 521003000000, 521004000000, 521005000000, 521006000000, 521007000000,
                    521008000000, 521009000000, 521010000000, 521011000000, 111111000000, 521013000000, 521014000000,
                    521015000000, 521016000000, 521017000000, 521018000000, 521019000000, 521020000000
                )])  # Nodes (Haltestellen ID's als "Knoten") in Graph H einfügen

                G.add_edges_from([
                    (520001000000, 520002000000), (520002000000, 520003000000), (520003000000, 520004000000),
                    (520004000000, 520005000000), (520005000000, 520006000000), (520006000000, 520007000000),
                    (520007000000, 520008000000), (520008000000, 520009000000), (520009000000, 520010000000),
                    (520010000000, 520011000000), (520011000000, 111111000000), (111111000000, 520013000000),
                    (520013000000, 520014000000), (520014000000, 520015000000), (520015000000, 520016000000),
                    (520016000000, 520017000000), (520017000000, 520018000000), (520018000000, 520019000000),
                    (520019000000, 520020000000), (520020000000, 520021000000), (520021000000, 520022000000),
                    (520022000000, 520023000000), (520002000000, 520001000000), (520003000000, 520002000000),
                    (520004000000, 520003000000), (520005000000, 520004000000), (520006000000, 520005000000),
                    (520007000000, 520006000000), (520008000000, 520007000000), (520009000000, 520008000000),
                    (520010000000, 520009000000), (520011000000, 520010000000), (111111000000, 520011000000),
                    (520013000000, 111111000000), (520014000000, 520013000000), (520015000000, 520014000000),
                    (520016000000, 520015000000), (520017000000, 520016000000), (520018000000, 520017000000),
                    (520019000000, 520018000000), (520020000000, 520019000000), (520021000000, 520020000000),
                    (520022000000, 520021000000), (520023000000, 520022000000)
                ])  # Edges ("Kanten") in Graph G einfügen

                H.add_edges_from([
                    (521001000000, 521002000000), (521002000000, 521003000000), (521003000000, 521004000000),
                    (521004000000, 521005000000), (521005000000, 521006000000), (521006000000, 521007000000),
                    (521007000000, 521008000000), (521008000000, 521009000000), (521009000000, 521010000000),
                    (521010000000, 521011000000), (521011000000, 111111000000), (111111000000, 521013000000),
                    (521013000000, 521014000000), (521014000000, 521015000000), (521015000000, 521016000000),
                    (521016000000, 521017000000), (521017000000, 521018000000), (521018000000, 521019000000),
                    (521019000000, 521020000000), (521002000000, 521001000000), (521003000000, 521002000000),
                    (521004000000, 521003000000), (521005000000, 521004000000), (521006000000, 521005000000),
                    (521007000000, 521006000000), (521008000000, 521007000000), (521009000000, 521008000000),
                    (521010000000, 521009000000), (521011000000, 521010000000), (111111000000, 521011000000),
                    (521013000000, 111111000000), (521014000000, 521013000000), (521015000000, 521014000000),
                    (521016000000, 521015000000), (521017000000, 521016000000), (521018000000, 521017000000),
                    (521019000000, 521018000000), (521020000000, 521019000000)
                ])  # Edges ("Kanten") in Graph G einfügen

                F = networkx.Graph()  # Initialisierung "leerer" Graph F (f. späteres Gesamtnetz)

                F.add_nodes_from(G)  # Hinzufügen der Nodes aus G
                F.add_nodes_from(H)  # Hinzufügen der Nodes aus H

                F.add_weighted_edges_from([
                    (520001000000, 520002000000, 0.369), (520002000000, 520003000000, 0.329),
                    (520003000000, 520004000000, 0.587),
                    (520004000000, 520005000000, 0.704), (520005000000, 520006000000, 0.898),
                    (520006000000, 520007000000, 2.530),
                    (520007000000, 520008000000, 1.150), (520008000000, 520009000000, 1.860),
                    (520009000000, 520010000000, 1.360),
                    (520010000000, 520011000000, 0.891), (520011000000, 111111000000, 1.520),
                    (111111000000, 520013000000, 2.540),
                    (520013000000, 520014000000, 1.180), (520014000000, 520015000000, 0.980),
                    (520015000000, 520016000000, 2.500),
                    (520016000000, 520017000000, 4.870), (520017000000, 520018000000, 1.830),
                    (520018000000, 520019000000, 1.420),
                    (520019000000, 520020000000, 1.790), (520020000000, 520021000000, 1.080),
                    (520021000000, 520022000000, 0.671),
                    (520022000000, 520023000000, 0.478), (520002000000, 520001000000, 0.369),
                    (520003000000, 520002000000, 0.329),
                    (520004000000, 520003000000, 0.587), (520005000000, 520004000000, 0.704),
                    (520006000000, 520005000000, 0.898),
                    (520007000000, 520006000000, 2.530), (520008000000, 520007000000, 1.150),
                    (520009000000, 520008000000, 1.860),
                    (520010000000, 520009000000, 1.360), (520011000000, 520010000000, 0.891),
                    (111111000000, 520011000000, 1.520),
                    (520013000000, 111111000000, 2.540), (520014000000, 520013000000, 1.180),
                    (520015000000, 520014000000, 0.980),
                    (520016000000, 520015000000, 2.500), (520017000000, 520016000000, 4.870),
                    (520018000000, 520017000000, 1.830),
                    (520019000000, 520018000000, 1.420), (520020000000, 520019000000, 1.790),
                    (520021000000, 520020000000, 1.080),
                    (520022000000, 520021000000, 0.671), (520023000000, 520022000000, 0.478),
                    (521001000000, 521002000000, 3.400),
                    (521002000000, 521003000000, 2.860), (521003000000, 521004000000, 0.821),
                    (521004000000, 521005000000, 1.370),
                    (521005000000, 521006000000, 1.740), (521006000000, 521007000000, 1.370),
                    (521007000000, 521008000000, 1.100),
                    (521008000000, 521009000000, 0.900), (521009000000, 521010000000, 1.290),
                    (521010000000, 521011000000, 2.710),
                    (521011000000, 111111000000, 1.130), (111111000000, 521013000000, 1.270),
                    (521013000000, 521014000000, 1.000),
                    (521014000000, 521015000000, 2.390), (521015000000, 521016000000, 1.870),
                    (521016000000, 521017000000, 4.780),
                    (521017000000, 521018000000, 2.790), (521018000000, 521019000000, 6.110),
                    (521019000000, 521020000000, 5.420),
                    (521002000000, 521001000000, 3.400), (521003000000, 521002000000, 2.860),
                    (521004000000, 521003000000, 0.821),
                    (521005000000, 521004000000, 1.370), (521006000000, 521005000000, 1.740),
                    (521007000000, 521006000000, 1.370),
                    (521008000000, 521007000000, 1.100), (521009000000, 521008000000, 0.900),
                    (521010000000, 521009000000, 1.290),
                    (521011000000, 521010000000, 2.710), (111111000000, 521011000000, 1.130),
                    (521013000000, 111111000000, 1.270),
                    (521014000000, 521013000000, 1.000), (521015000000, 521014000000, 2.390),
                    (521016000000, 521015000000, 1.870),
                    (521017000000, 521016000000, 4.780), (521018000000, 521017000000, 2.790),
                    (521019000000, 521018000000, 6.110),
                    (521020000000, 521019000000, 5.420)
                ])  # "gewichtete" Kanten (= Menge der Kanten aus G und H, jeweils mit Länge in km)
                # zu Graph F hinzufügen. Muster: (Knoten 1, Knoten 2, Länge) --> "Hin"-Paket,
                # (Knoten 2, Knoten 1, Länge) --> "Rück"-Paket (Länge identisch).
                # sämtliche Entfernungsangaben kommen für jede Linie also doppelt vor.

                print(F.size(
                    weight="weight"))  # Summe aller Längen ("weights") in F, Länge d. Strckennetzes: Resultat geteilt durch 2

                E = networkx.Graph()  # Initialisierung "leerer" Graph E ("Container" f. Resultat aus Fahrplanauskunft)

                list_1 = networkx.shortest_path(F, int(StartPoint), int(EndPoint))
                print(len(list_1))
                E.add_nodes_from(list_1)  # Kürzester von A nach B (Grundlage für Fahrplanauskunft)
                print(E)  # Anzahl der Haltestellen (inkl. Ein- und Ausstieg)
                valx = ""
                valy = ""
                for i in range(len(list_1)):
                    val1 = Haltestelle.objects.raw("SELECT ST_X(location) as xvalue, ST_Y(location) as yvalue, name as info, hid as id FROM network_haltestelle WHERE hid LIKE '%s'", [list_1[i]])
                    for x in val1:
                        valy = str(x.xvalue)
                    for y in val1:
                        valx = str(y.yvalue)
                    if i != 0:
                        routenpunkte += str(", ")
                    i = i + 1
                    routenpunkte += str("[")
                    routenpunkte += str(valx)
                    routenpunkte += str(", ")
                    routenpunkte += str(valy)
                    routenpunkte += str("]")
                    #testxy.append(valx)
                print(routenpunkte)



    context = {'Line1': Line1, 'Line2': Line2, 'Caseritz': Caseritz, 'All': All, 'route': route, 'routenpunkte': routenpunkte}
    return render(request, 'index.html', context)

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import os

class Triangle():
    def __init__(self, p1, p2, p3):
        self.v = [p1, p2, p3]
        self.e = [(p1, p2), (p2, p3), (p3, p1)]
    def has_edge(self, edge):
        return (edge[0], edge[1]) in self.e or (edge[1], edge[0]) in self.e

    def has_vertex(self, v):
        return v in self.v

def get_circumcircle_center(triangle):
    A = triangle.v[1][0] - triangle.v[0][0]
    B = triangle.v[1][1] - triangle.v[0][1]
    C = triangle.v[2][0] - triangle.v[0][0]
    D = triangle.v[2][1] - triangle.v[0][1]
    E = A * (triangle.v[1][0] + triangle.v[0][0]) + B * (triangle.v[1][1] +triangle.v[0][1])
    F = C * (triangle.v[2][0] + triangle.v[0][0]) + D * (triangle.v[2][1] + triangle.v[0][1])
    G = 2 * (A * (triangle.v[2][1] - triangle.v[1][1]) - B * (triangle.v[2][0] - triangle.v[1][0]))
    if G == 0:
        (0, 0, 10**9)
    Cx = (D * E - B * F) / G
    Cy = (A * F - C * E) / G
    R = ((Cx - triangle.v[0][0])**2 + (Cy - triangle.v[0][1])**2)**(1/2)
    return (Cx, Cy, R)

def online_bowyer_watson(triangulation, point):
    bad_triangles = []
    for triangle in triangulation:
        cx, cy, r = get_circumcircle_center(triangle)
        if (point[0] - cx) ** 2 + (point[1] - cy)**2 <= r**2:
            bad_triangles.append(triangle)

    polygon = []
    for triangle in bad_triangles:
        for edge in triangle.e:
            is_shared = False
            for other in bad_triangles:
                if triangle == other:
                    continue
                if other.has_edge(edge):
                    is_shared = True
            if not is_shared:
                polygon.append(edge)

    for triangle in bad_triangles:
        triangulation.remove(triangle)

    for edge in polygon:
        triangulation.add(Triangle(edge[0], edge[1], point))

    return triangulation

def plot_triangulation(super_triangle, triangulation, step, points):
    edges = []
    fig, ax = plt.subplots()

    ax.scatter(*zip(*points))
    for triangle in triangulation:
        if triangle.has_vertex(super_triangle.v[0]) \
            or triangle.has_vertex(super_triangle.v[1]) \
            or triangle.has_vertex(super_triangle.v[2]):
            continue

        edges.append(triangle.e[0])
        edges.append(triangle.e[1])
        edges.append(triangle.e[2])

    lc = LineCollection(edges)
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    plt.savefig("./delaunay_plots/delaunay_triangulation_{}.png".format(step), format='png')

if __name__ == "__main__":
    if not os.path.exists('delaunay_plots'):
        os.makedirs('delaunay_plots')
    width = int(input('Ширина:'))
    height = int(input('Высота:'))
    super_triangle = Triangle((-100, -100), (2*width + 100,  -100), (-100, 2*height + 100))
    points = []
    triangulation = set([super_triangle])
    while(True):
        p = input("Введите новую точку или exit для выхода: ")
        if p == 'exit':
            break
        point = tuple(map(float, p.split()))
        points.append(point)
        triangulation = online_bowyer_watson(triangulation, point)
        if len(points) >= 3:
            plot_triangulation(super_triangle, triangulation, len(points), points)

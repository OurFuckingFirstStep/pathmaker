#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lxml import etree
import copy

nsmap = {
    'sodipodi': 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
    'cc': 'http://web.resource.org/cc/',
    'svg': 'http://www.w3.org/2000/svg',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'xlink': 'http://www.w3.org/1999/xlink',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'inkscape': 'http://www.inkscape.org/namespaces/inkscape'
}


class UnknownVertex(Exception):
    pass


class NoPath(Exception):
    pass


class PathMap(object):
    """
    В .svg файле все пути имеют тег <path> и id="2and5",
    где числа обозначают контрольные точки.
    """
    def __init__(self, in_file_svg):
        doc = etree.parse(in_file_svg)

        # Create graph like dict
        graph = {}
        paths = doc.xpath('//svg:path', namespaces=nsmap)
        for path in paths:
            id1, id2 = path.get('id').split('and')
            if id1 not in graph:
                graph[id1] = set()
            graph[id1].add(id2)
            if id2 not in graph:
                graph[id2] = set()
            graph[id2].add(id1)
            path.set('visibility', 'hidden')
        self.graph = graph.copy()

        self.doc = doc

    def create_path(self, id1, id2, out_file_svg=None):
        """
        Return .svg if out_file_svg is not None,
        otherwise, None
        """
        def _deep_search(id1, id2, parents_id):
            paths = []
            for item in self.graph[id1]:
                if item in parents_id:
                    continue
                elif item == id2:
                    paths.append([id1, id2])
                else:
                    parents_id.append(item)
                    path_pre = _deep_search(item, id2, parents_id)
                    if path_pre != []:
                        for item_pre in path_pre:
                            item_pre.insert(0, id1)
                            paths.append(item_pre)
                    parents_id.remove(item)
            return paths

        if isinstance(id1, int):
            id1 = str(id1)
        if isinstance(id2, int):
            id2 = str(id2)
        if id1 == id2:
            return

        if id1 not in self.graph:
            raise UnknownVertex
        if id2 not in self.graph:
            raise UnknownVertex

        paths = _deep_search(id1, id2, [id1])
        if paths == []:
            raise NoPath
        path = min(paths, key=len)
        doc = copy.deepcopy(self.doc)

        it = iter(path)
        lst, rst = next(it, False), next(it, False)
        while rst:
            elem = doc.xpath(
                "//svg:path[@id='" + lst + "and" + rst + "']",
                namespaces=nsmap
            )
            if elem == []:
                elem = doc.xpath(
                    "//svg:path[@id='" + rst + "and" + lst + "']",
                    namespaces=nsmap
                )
            elem[0].set('visibility', 'visible')
            lst, rst = rst, next(it, False)

        if out_file_svg is not None:
            with open(out_file_svg, 'wb') as pf:
                doc.write(pf)
        else:
            return etree.tostring(doc)

if __name__ == "__main__":
    path = PathMap("image.svg")
    path.create_path(1, 7, "image_path_17.svg")
    path.create_path(3, 7, "image_path_37.svg")
    path.create_path(1, 2, "image_path_12.svg")
    path.create_path(2, 1, "image_path_21.svg")
    path.create_path(4, 6, "image_path_46.svg")
    path.create_path("4", "6", "image_path_46.svg")
    path.create_path("6", "4", "image_path_64.svg")
    byte_string = path.create_path("6", "4")
    with open("image_path_64.svg", 'wb') as pf:
        pf.write(byte_string)

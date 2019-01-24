#!/usr/bin/env python2
# -*- coding: utf-8 -*-

class CollinsSpan:

    def __init__(self, i, j, k, h, score):
        self.i = i
        self.j = j
        self.k = k
        self.h = h
        self.score = score

    def __str__(self):
        return "[%s, %s, %s, %s, %s]" % (self.i, self.j, self.k, self.h, self.score)


class CollinsParser:

    def __init__(self):
        self.chart = None

    def parse(self, words):
        self.words = words
        self.init_spans(words)
        self.heads = [None for i in range(len(words))]

        # merge spans in a bottom-up manner
        for l in xrange(1, len(words)+1):
            for i in xrange(0, len(words)):
                j = i + l
                if j > len(words): break
                for k in xrange(i+1, j):
                    for h_l in xrange(i, k):
                        for h_r in xrange(k, j):
                            span_l = self.chart[i][k][h_l]
                            span_r = self.chart[k][j][h_r]
                            # l -> r
                            score = self.get_score(words, span_l, span_r)
                            span = CollinsSpan(i, j, k, h_l, score)
                            self.add_span(span)
                            # r -> l
                            score = self.get_score(words, span_r, span_l)
                            span = CollinsSpan(i, j, k, h_r, score)
                            self.add_span(span)
        #top layer
        self.best_top_layer_span = self.find_best(0, len(words)) 
        self.backtrace(self.best_top_layer_span)

    def backtrace(self, span):
        # trace back to left
        self.trace_direction(span, 'left')
        # trace back to right
        self.trace_direction(span, 'right')

    def trace_direction(self, upper_span, direction):
        if direction == 'left':
            current_span = self.find_best(upper_span.i, upper_span.k)
        elif direction == 'right':
            current_span = self.find_best(upper_span.k, upper_span.j)

        # dicide heads
        if upper_span.h != current_span.i:
            self.heads[current_span.i] = upper_span.h
        elif upper_span.h != current_span.j - 1:
            self.heads[current_span.j - 1] = upper_span.h

        if current_span.j - current_span.i > 1:
            self.backtrace(current_span)
        else:
            pass

    def print_heads(self):
        head_words = []
        #print(self.heads)
        for i in self.heads:
            try:
                head_words.append(self.words[i])
            except TypeError:
                head_words.append(None)
        print(head_words)

    def init_spans(self, words):
        # initialize chart as 3-dimensional list
        length = len(words) + 1
        chart = []
        for i in xrange(length):
            chart.append([])
            for j in xrange(length):
                chart[i].append([None] * length)
        self.chart = chart

        # add 1-length spans to the chart
        for i in xrange(0, len(words)):
            span = CollinsSpan(i, i+1, i, i, 0.0)
            self.add_span(span)

    def add_span(self, new_span):
        i, j, h = new_span.i, new_span.j, new_span.h
        old_span = self.chart[i][j][h]
        if old_span is None or old_span.score < new_span.score:
            self.chart[i][j][h] = new_span # update chart

    def get_score(self, words, head, dep):
        # currently, use naive scoring function
        h_word = words[head.h]
        if h_word == "read":
            score = 1.0
        elif h_word == "novel":
            score = 1.0
        else:
            score = 0.0
        # calculate score based on arc-factored model
        return head.score + dep.score + score

    """ Find the highest-scored span [i, j, h] from [i, j] """
    def find_best(self, i, j):
        best_span = None
        for h in xrange(i, j):
            span = self.chart[i][j][h]
            if best_span is None or best_span.score < span.score:
                best_span = span
        return best_span

# run
p = CollinsParser()
p.parse(["She", "read", "a", "short", "novel"])
p.print_heads()

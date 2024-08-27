#ifndef __INTERVAL_TREE_H
#define __INTERVAL_TREE_H

#include <vector>
#include <algorithm>
#include <iostream>
#include <memory>
#include <cassert>
#include <limits>

#ifdef USE_INTERVAL_TREE_NAMESPACE
namespace interval_tree {
#endif

template <class Scalar, typename Value>
class Interval {
public:
    Scalar start;
    Scalar stop;
    Value value;

    Interval(const Scalar& s, const Scalar& e, const Value& v)
        : start(std::min(s, e)), stop(std::max(s, e)), value(v) {}
};

template <class Scalar, typename Value>
Scalar intervalStart(const Interval<Scalar, Value>& i) {
    return i.start;
}

template <class Scalar, typename Value>
Scalar intervalStop(const Interval<Scalar, Value>& i) {
    return i.stop;
}

template <class Scalar, typename Value>
std::ostream& operator<<(std::ostream& out, const Interval<Scalar, Value>& i) {
    out << "Interval(" << i.start << ", " << i.stop << "): " << i.value;
    return out;
}

template <class Scalar, class Value>
class IntervalTree {
public:
    typedef Interval<Scalar, Value> interval;
    typedef std::vector<interval> interval_vector;

    struct IntervalStartCmp {
        bool operator()(const interval& a, const interval& b) const {
            return a.start < b.start;
        }
    };

    struct IntervalCompVal {
        bool operator()(const interval& a, const interval& b) const {
            return a.value < b.value;
        }
    };

    struct IntervalStopCmp {
        bool operator()(const interval& a, const interval& b) const {
            return a.stop < b.stop;
        }
    };

    IntervalTree()
        : root(nullptr) {}

    IntervalTree(interval_vector&& ivals)
        : root(nullptr) {
        for (auto& i : ivals) {
            insert(i);
        }
    }

    ~IntervalTree() = default;

    IntervalTree(const IntervalTree& other)
        : root(clone(other.root)) {}

    IntervalTree& operator=(const IntervalTree& other) {
        if (this != &other) {
            root = clone(other.root);
        }
        return *this;
    }

    IntervalTree(IntervalTree&&) = default;
    IntervalTree& operator=(IntervalTree&&) = default;

    // Insert a new interval
    void insert(const interval& i) {
        root = insert(std::move(root), i);
        root->color = false; // root is always black
    }

    // Find all intervals overlapping with [start, stop]
    interval_vector findOverlapping(const Scalar& start, const Scalar& stop, bool sort = false) const {
        interval_vector result;
        visit_overlapping(root.get(), start, stop, [&](const interval& i) { result.push_back(i); });
        if (sort) std::sort(result.begin(), result.end(), IntervalStartCmp());
        return result;
    }

    // Find all values of intervals overlapping with [start, stop]
    std::vector<Value> findOverlappingValues(const Scalar& start, const Scalar& stop) const {
        std::vector<Value> result;
        interval_vector result_intervals;
        visit_overlapping(root.get(), start, stop, [&](const interval& i) { result_intervals.push_back(i); });
        std::sort(result_intervals.begin(), result_intervals.end(), IntervalCompVal());
        for (const auto& i : result_intervals) result.push_back(i.value);
        return result;
    }

    // Find all intervals contained within [start, stop]
    interval_vector findContained(const Scalar& start, const Scalar& stop, bool sort = false) const {
        interval_vector result;
        visit_contained(root.get(), start, stop, [&](const interval& i) { result.push_back(i); });
        if (sort) std::sort(result.begin(), result.end(), IntervalStartCmp());
        return result;
    }

    bool empty() const {
        return !root;
    }

    friend std::ostream& operator<<(std::ostream& os, const IntervalTree& itree) {
        return writeOut(os, itree);
    }

private:
    struct Node {
        interval data;
        Scalar max_right;
        std::unique_ptr<Node> left;
        std::unique_ptr<Node> right;
        bool color; // Red-Black Tree color: true for red, false for black

        Node(const interval& i)
            : data(i), max_right(i.stop), left(nullptr), right(nullptr), color(true) {}
    };

    std::unique_ptr<Node> root;

    // Red-Black Tree functions
    bool is_red(const std::unique_ptr<Node>& node) const {
        return node && node->color;
    }

    std::unique_ptr<Node> rotate_left(std::unique_ptr<Node> h) {
        std::unique_ptr<Node> x = std::move(h->right);
        h->right = std::move(x->left);
        x->left = std::move(h);
        x->color = x->left->color;
        x->left->color = true;
        return x;
    }

    std::unique_ptr<Node> rotate_right(std::unique_ptr<Node> h) {
        std::unique_ptr<Node> x = std::move(h->left);
        h->left = std::move(x->right);
        x->right = std::move(h);
        x->color = x->right->color;
        x->right->color = true;
        return x;
    }

    void flip_colors(Node* h) {
        h->color = !h->color;
        if (h->left) h->left->color = !h->left->color;
        if (h->right) h->right->color = !h->right->color;
    }

    std::unique_ptr<Node> insert(std::unique_ptr<Node> node, const interval& i) {
        if (!node) {
            return std::make_unique<Node>(i);
        }

        if (i.start < node->data.start) {
            node->left = insert(std::move(node->left), i);
        } else if (i.start > node->data.start || (i.start == node->data.start && i.stop > node->data.stop)) {
            node->right = insert(std::move(node->right), i);
        } else {
            node->data = i; // Replace existing interval with the new one
        }

        if (is_red(node->right) && !is_red(node->left)) node = rotate_left(std::move(node));
        if (is_red(node->left) && is_red(node->left->left)) node = rotate_right(std::move(node));
        if (is_red(node->left) && is_red(node->right)) flip_colors(node.get());

        node->max_right = std::max({node->data.stop, max_right(node->left), max_right(node->right)});
        return node;
    }

    Scalar max_right(const std::unique_ptr<Node>& node) const {
        return node ? node->max_right : std::numeric_limits<Scalar>::min();
    }

    std::unique_ptr<Node> clone(const std::unique_ptr<Node>& node) const {
        if (!node) return nullptr;
        auto new_node = std::make_unique<Node>(node->data);
        new_node->left = clone(node->left);
        new_node->right = clone(node->right);
        new_node->color = node->color;
        new_node->max_right = node->max_right;
        return new_node;
    }

    // Helper functions for visit
    template <class UnaryFunction>
    void visit_near(const Node* node, const Scalar& start, const Scalar& stop, UnaryFunction f) const {
        if (!node) return;

        if (!node->left && !node->right && node->data.stop >= start && node->data.start <= stop) {
            f(node->data);
        }

        if (node->left && start <= node->left->max_right) {
            visit_near(node->left.get(), start, stop, f);
        }
        if (node->right && node->data.start <= stop) {
            visit_near(node->right.get(), start, stop, f);
        }
    }

    template <class UnaryFunction>
    void visit_overlapping(const Node* node, const Scalar& start, const Scalar& stop, UnaryFunction f) const {
        if (!node) return;

        if (node->data.stop > start && node->data.start < stop) {
            f(node->data);
        }

        if (node->left && start < node->left->max_right) {
            visit_overlapping(node->left.get(), start, stop, f);
        }

        if (node->right && node->data.start < stop) {
            visit_overlapping(node->right.get(), start, stop, f);
        }
    }
};

#ifdef USE_INTERVAL_TREE_NAMESPACE
}
#endif

#endif

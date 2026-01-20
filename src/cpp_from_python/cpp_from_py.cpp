/*
 * Learn C++ from Python - Modern C++ Examples with Tests
 *
 * Demonstrates modern C++ syntax with Python equivalents in Doxygen comments.
 * Build: mkdir build && cd build && cmake .. && make
 * Test: make test
 */

#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <algorithm>
#include <numeric>
#include <optional>
#include <memory>
#include <tuple>
#include <functional>
#include <gtest/gtest.h>

/**
 * @brief Print hello world message
 *
 * Python equivalent:
 * @code{.py}
 * print("Hello, World!")
 * @endcode
 */
void hello_world() {
    std::cout << "Hello, World!" << std::endl;
}

/**
 * @brief Demonstrate automatic type inference with auto keyword
 *
 * Python equivalent:
 * @code{.py}
 * x = 10
 * y = 3.14
 * name = "Alice"
 * is_valid = True
 * @endcode
 */
void variables() {
    auto x = 10;
    auto y = 3.14;
    auto name = "Alice";
    auto is_valid = true;
}

/**
 * @brief Create and manipulate vectors (dynamic arrays)
 *
 * Python equivalent:
 * @code{.py}
 * numbers = [1, 2, 3, 4, 5]
 * numbers.append(6)
 * print(numbers[0])
 * print(len(numbers))
 * @endcode
 */
std::vector<int> lists_and_vectors() {
    std::vector<int> numbers = {1, 2, 3, 4, 5};
    numbers.push_back(6);
    return numbers;
}

/**
 * @brief Demonstrate array slicing and access patterns
 *
 * Python equivalent:
 * @code{.py}
 * numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
 * print(numbers[0])
 * print(numbers[-1])
 * print(numbers[2:5])
 * print(numbers[:3])
 * print(numbers[7:])
 * print(numbers[::2])
 * print(numbers[::-1])
 * @endcode
 */
std::vector<int> array_slicing() {
    std::vector<int> numbers = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};

    // Slicing [2:5]
    std::vector<int> slice(numbers.begin() + 2, numbers.begin() + 5);

    // Every second element [::2]
    std::vector<int> every_second;
    for (size_t i = 0; i < numbers.size(); i += 2) {
        every_second.push_back(numbers[i]);
    }

    // Reversed [::-1]
    std::vector<int> reversed(numbers.rbegin(), numbers.rend());

    return reversed;
}

/**
 * @brief Use maps for key-value storage
 *
 * Python equivalent:
 * @code{.py}
 * ages = {"Alice": 30, "Bob": 25}
 * ages["Charlie"] = 35
 * print(ages["Alice"])
 * @endcode
 */
std::map<std::string, int> dictionaries_and_maps() {
    std::map<std::string, int> ages = {{"Alice", 30}, {"Bob", 25}};
    ages["Charlie"] = 35;
    return ages;
}

/**
 * @brief Range-based for loops
 *
 * Python equivalent:
 * @code{.py}
 * for i in range(5):
 *     print(i)
 *
 * for item in [1, 2, 3]:
 *     print(item)
 * @endcode
 */
void for_loop() {
    for (int i = 0; i < 5; i++) {
        // Traditional loop
    }

    for (auto item : {1, 2, 3}) {
        // Range-based loop
    }
}

/**
 * @brief Add two numbers
 *
 * Python equivalent:
 * @code{.py}
 * def add(a, b):
 *     return a + b
 *
 * result = add(3, 5)
 * @endcode
 */
auto add(int a, int b) -> int {
    return a + b;
}

/**
 * @brief Lambda function that squares a number
 *
 * Python equivalent:
 * @code{.py}
 * square = lambda x: x * x
 * print(square(5))
 *
 * numbers = [1, 2, 3, 4]
 * squared = list(map(lambda x: x * x, numbers))
 *
 * multiplier = 10
 * multiply = lambda x: x * multiplier
 * print(multiply(5))
 * @endcode
 */
std::function<int(int)> create_square_lambda() {
    return [](int x) { return x * x; };
}

/**
 * @brief Lambda with variable capture
 *
 * Python equivalent:
 * @code{.py}
 * multiplier = 10
 * multiply = lambda x: x * multiplier
 * @endcode
 */
std::function<int(int)> create_multiply_lambda(int multiplier) {
    return [multiplier](int x) { return x * multiplier; };
}

/**
 * @brief Transform vector using lambda
 *
 * Python equivalent:
 * @code{.py}
 * numbers = [1, 2, 3, 4]
 * squared = list(map(lambda x: x * x, numbers))
 * @endcode
 */
std::vector<int> transform_with_lambda(const std::vector<int>& numbers) {
    std::vector<int> squared;
    std::transform(numbers.begin(), numbers.end(),
                   std::back_inserter(squared),
                   [](int x) { return x * x; });
    return squared;
}

/**
 * @brief List comprehension equivalent
 *
 * Python equivalent:
 * @code{.py}
 * squares = [x * x for x in range(10)]
 * evens = [x for x in range(10) if x % 2 == 0]
 * @endcode
 */
std::vector<int> list_comprehension() {
    std::vector<int> evens;
    for (int x = 0; x < 10; x++) {
        if (x % 2 == 0) {
            evens.push_back(x);
        }
    }
    return evens;
}

/**
 * @brief String concatenation and manipulation
 *
 * Python equivalent:
 * @code{.py}
 * s = "Hello"
 * s += " World"
 * print(len(s))
 * print(s[0])
 * @endcode
 */
std::string string_operations() {
    std::string s = "Hello";
    s += " World";
    return s;
}

/**
 * @brief Person class with constructor and method
 *
 * Python equivalent:
 * @code{.py}
 * class Person:
 *     def __init__(self, name, age):
 *         self.name = name
 *         self.age = age
 *
 *     def greet(self):
 *         return f"Hello, I'm {self.name}"
 *
 * p = Person("Alice", 30)
 * print(p.greet())
 * @endcode
 */
class Person {
public:
    std::string name;
    int age;

    Person(std::string name, int age);
    std::string greet() const;
};

Person::Person(std::string n, int a) : name(n), age(a) {}

std::string Person::greet() const {
    return "Hello, I'm " + name;
}

/**
 * @brief Optional value handling
 *
 * Python equivalent:
 * @code{.py}
 * def find_value(key):
 *     data = {"a": 1, "b": 2}
 *     return data.get(key)
 *
 * result = find_value("a")
 * if result is not None:
 *     print(result)
 * @endcode
 */
std::optional<int> find_value(const std::string& key) {
    std::map<std::string, int> data = {{"a", 1}, {"b", 2}};
    auto it = data.find(key);
    if (it != data.end()) {
        return it->second;
    }
    return std::nullopt;
}

/**
 * @brief Tuple unpacking with structured bindings
 *
 * Python equivalent:
 * @code{.py}
 * point = (10, 20)
 * x, y = point
 * print(x, y)
 * @endcode
 */
std::tuple<int, int> create_tuple() {
    return std::make_tuple(10, 20);
}

/**
 * @brief Filter even numbers from vector
 *
 * Python equivalent:
 * @code{.py}
 * numbers = [1, 2, 3, 4, 5]
 * evens = list(filter(lambda x: x % 2 == 0, numbers))
 * @endcode
 */
std::vector<int> filter_evens(const std::vector<int>& numbers) {
    std::vector<int> evens;
    std::copy_if(numbers.begin(), numbers.end(),
                 std::back_inserter(evens),
                 [](int x) { return x % 2 == 0; });
    return evens;
}

/**
 * @brief Check if any element satisfies condition
 *
 * Python equivalent:
 * @code{.py}
 * numbers = [1, 2, 3, 4, 5]
 * has_even = any(x % 2 == 0 for x in numbers)
 * @endcode
 */
bool has_even(const std::vector<int>& numbers) {
    return std::any_of(numbers.begin(), numbers.end(),
                       [](int x) { return x % 2 == 0; });
}

/**
 * @brief Check if all elements satisfy condition
 *
 * Python equivalent:
 * @code{.py}
 * numbers = [1, 2, 3, 4, 5]
 * all_positive = all(x > 0 for x in numbers)
 * @endcode
 */
bool all_positive(const std::vector<int>& numbers) {
    return std::all_of(numbers.begin(), numbers.end(),
                       [](int x) { return x > 0; });
}

/**
 * @brief Sort vector in place
 *
 * Python equivalent:
 * @code{.py}
 * numbers = [3, 1, 4, 1, 5]
 * numbers.sort()
 * @endcode
 */
std::vector<int> sort_vector(std::vector<int> numbers) {
    std::sort(numbers.begin(), numbers.end());
    return numbers;
}

/**
 * @brief Find minimum element
 *
 * Python equivalent:
 * @code{.py}
 * numbers = [3, 1, 4, 1, 5]
 * print(min(numbers))
 * @endcode
 */
int find_min(const std::vector<int>& numbers) {
    return *std::min_element(numbers.begin(), numbers.end());
}

/**
 * @brief Sum all elements
 *
 * Python equivalent:
 * @code{.py}
 * numbers = [1, 2, 3, 4, 5]
 * total = sum(numbers)
 * @endcode
 */
int sum_vector(const std::vector<int>& numbers) {
    return std::accumulate(numbers.begin(), numbers.end(), 0);
}

/**
 * @brief Function with default argument
 *
 * Python equivalent:
 * @code{.py}
 * def greet(name, greeting="Hello"):
 *     return f"{greeting}, {name}"
 *
 * print(greet("Alice"))
 * print(greet("Bob", "Hi"))
 * @endcode
 */
std::string greet(const std::string& name, const std::string& greeting = "Hello") {
    return greeting + ", " + name;
}

TEST(BasicTest, AddFunction) {
    EXPECT_EQ(add(3, 5), 8);
    EXPECT_EQ(add(0, 0), 0);
    EXPECT_EQ(add(-1, 1), 0);
}

TEST(VectorTest, ListsAndVectors) {
    auto vec = lists_and_vectors();
    EXPECT_EQ(vec.size(), 6);
    EXPECT_EQ(vec[0], 1);
    EXPECT_EQ(vec[5], 6);
}

TEST(VectorTest, ArraySlicing) {
    auto reversed = array_slicing();
    EXPECT_EQ(reversed.size(), 10);
    EXPECT_EQ(reversed[0], 9);
    EXPECT_EQ(reversed[9], 0);
}

TEST(MapTest, DictionariesAndMaps) {
    auto ages = dictionaries_and_maps();
    EXPECT_EQ(ages["Alice"], 30);
    EXPECT_EQ(ages["Bob"], 25);
    EXPECT_EQ(ages["Charlie"], 35);
}

TEST(LambdaTest, SquareLambda) {
    auto square = create_square_lambda();
    EXPECT_EQ(square(5), 25);
    EXPECT_EQ(square(0), 0);
    EXPECT_EQ(square(-3), 9);
}

TEST(LambdaTest, MultiplyLambda) {
    auto multiply = create_multiply_lambda(10);
    EXPECT_EQ(multiply(5), 50);
    EXPECT_EQ(multiply(0), 0);
}

TEST(LambdaTest, TransformWithLambda) {
    std::vector<int> numbers = {1, 2, 3, 4};
    auto squared = transform_with_lambda(numbers);
    EXPECT_EQ(squared.size(), 4);
    EXPECT_EQ(squared[0], 1);
    EXPECT_EQ(squared[1], 4);
    EXPECT_EQ(squared[2], 9);
    EXPECT_EQ(squared[3], 16);
}

TEST(VectorTest, ListComprehension) {
    auto evens = list_comprehension();
    EXPECT_EQ(evens.size(), 5);
    EXPECT_EQ(evens[0], 0);
    EXPECT_EQ(evens[4], 8);
}

TEST(StringTest, StringOperations) {
    auto str = string_operations();
    EXPECT_EQ(str, "Hello World");
    EXPECT_EQ(str.size(), 11);
}

TEST(ClassTest, PersonClass) {
    Person p("Alice", 30);
    EXPECT_EQ(p.name, "Alice");
    EXPECT_EQ(p.age, 30);
    EXPECT_EQ(p.greet(), "Hello, I'm Alice");
}

TEST(OptionalTest, FindValue) {
    auto result = find_value("a");
    ASSERT_TRUE(result.has_value());
    EXPECT_EQ(result.value(), 1);

    auto missing = find_value("z");
    EXPECT_FALSE(missing.has_value());
}

TEST(TupleTest, CreateTuple) {
    auto [x, y] = create_tuple();
    EXPECT_EQ(x, 10);
    EXPECT_EQ(y, 20);
}

TEST(AlgorithmTest, FilterEvens) {
    std::vector<int> numbers = {1, 2, 3, 4, 5};
    auto evens = filter_evens(numbers);
    EXPECT_EQ(evens.size(), 2);
    EXPECT_EQ(evens[0], 2);
    EXPECT_EQ(evens[1], 4);
}

TEST(AlgorithmTest, HasEven) {
    std::vector<int> with_even = {1, 2, 3};
    std::vector<int> without_even = {1, 3, 5};
    EXPECT_TRUE(has_even(with_even));
    EXPECT_FALSE(has_even(without_even));
}

TEST(AlgorithmTest, AllPositive) {
    std::vector<int> all_pos = {1, 2, 3};
    std::vector<int> has_neg = {1, -2, 3};
    EXPECT_TRUE(all_positive(all_pos));
    EXPECT_FALSE(all_positive(has_neg));
}

TEST(AlgorithmTest, SortVector) {
    std::vector<int> unsorted = {3, 1, 4, 1, 5};
    auto sorted = sort_vector(unsorted);
    EXPECT_EQ(sorted[0], 1);
    EXPECT_EQ(sorted[4], 5);
}

TEST(AlgorithmTest, FindMin) {
    std::vector<int> numbers = {3, 1, 4, 1, 5};
    EXPECT_EQ(find_min(numbers), 1);
}

TEST(AlgorithmTest, SumVector) {
    std::vector<int> numbers = {1, 2, 3, 4, 5};
    EXPECT_EQ(sum_vector(numbers), 15);
}

TEST(FunctionTest, DefaultArguments) {
    EXPECT_EQ(greet("Alice"), "Hello, Alice");
    EXPECT_EQ(greet("Bob", "Hi"), "Hi, Bob");
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

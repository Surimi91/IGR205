#include <SFML/Graphics.hpp>
#include <iostream>
#include <vector>
#include <random>

// constantes
const double d1 = 1;
const double d2 = 0.5;
const double f = 0.035;
const double k = 0.058;
const int rows = 500;
const int columns = 500;
const int pixelSize = 1;

// Kernel
double kernel3[3][3] = {
    {0.05, 0.2, 0.05},
    {0.2, -1, 0.2},
    {0.05, 0.2, 0.05}
};


int wrap(int a, int limit) {
    return (a + limit)%limit;
}


void update(std::vector<std::vector<double> >& A, std::vector<std::vector<double> >& B) {
    std::vector<std::vector<double> > A_next(rows, std::vector<double>(columns));
    std::vector<std::vector<double> > B_next(rows, std::vector<double>(columns));

    for (int r = 0; r < rows; ++r) {
        for (int c = 0; c < columns; ++c) {
            double aExtra = 0;
            double bExtra = 0;

            // convolution
            for (int i = -1; i <= 1; ++i) {
                for (int j = -1; j <= 1; ++j) {
                    int wrappedR = wrap(r + i, rows);
                    int wrappedC = wrap(c + j, columns);
                    aExtra += A[wrappedR][wrappedC] * kernel3[i + 1][j + 1];
                    bExtra += B[wrappedR][wrappedC] * kernel3[i + 1][j + 1];
                }
            }

            A_next[r][c] = A[r][c] + d1 * aExtra - A[r][c] * B[r][c] * B[r][c] + f * (1 - A[r][c]);
            B_next[r][c] = B[r][c] + d2 * bExtra + A[r][c] * B[r][c] * B[r][c] - (f + k) * B[r][c];
        }
    }

    A = A_next;
    B = B_next;
}

// initialization grid
void setup(std::vector<std::vector<double> >& A, std::vector<std::vector<double> >& B) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distrib(0, 100);

    for (int r = 0; r < rows; ++r) {
        for (int c = 0; c < columns; ++c) {
            A[r][c] = 1;
            B[r][c] = 0;
            if (distrib(gen) < 4) {
                A[r][c] = 0;
                B[r][c] = 1;
            }
        }
    }
}

int main() {
    std::vector<std::vector<double> > A(rows, std::vector<double>(columns));
    std::vector<std::vector<double> > B(rows, std::vector<double>(columns));

    setup(A, B);

    //500 updates
    for (int i = 0; i < 500; ++i) {
        update(A, B);
    }



    sf::RenderWindow window(sf::VideoMode(columns * pixelSize, rows * pixelSize), "Simulation Results");

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        window.clear();

        for (int r = 0; r < rows; ++r) {
            for (int c = 0; c < columns; ++c) {
                sf::RectangleShape pixel(sf::Vector2f(pixelSize, pixelSize));
                pixel.setPosition(c * pixelSize, r * pixelSize);
                pixel.setFillColor(sf::Color(std::min(255.0, A[r][c] * 255), std::min(255.0, B[r][c] * 255), 0));
                window.draw(pixel);
            }
        }

        window.display();
    }

    return 0;
}
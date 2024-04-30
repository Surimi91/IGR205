#include <SFML/Graphics.hpp>
#include <iostream>
#include <vector>
#include <random>
#include <fstream>
#include <sstream>
#include <string>



// constantes
const float r1 = 0.396;
const float r2 = 0.588;

const int c2=1;
const int c1=2;

double sumY;

const int rows = 200;
const int columns = 200;
const int pixelSize = 1;

// Kernel
double kernel5[5][5] = {
    {-0.25, -1.0, -1.5, -1.0, -0.25},
    {-1.0, 2.5, 7.0, 2.5, -1.0},
    {-1.5, 7.0, -23.5, 7.0, -1.5},
    {-1.0, 2.5, 7.0, 2.5, -1.0},
    {-0.25, -1.0, -1.5, -1.0, -0.25}
};

//pour la convolution et le calcul de X(t+1)
std::vector<std::vector<double> > Y(rows, std::vector<double>(columns));
std::vector<std::vector<double> > Y_convo(rows, std::vector<double>(columns));


int wrap(int a, int limit) {
    return (a + limit)%limit;
}




//pour l'initialisation de la grille via python
//doit être en nuances de gris absolument
void loadCSV(std::vector<std::vector<double> >& X, std::vector<std::vector<double> >& I, const std::string& filename) {
    std::ifstream file(filename);
    std::string line;
    int r = 0;

    if (!file.is_open()) {std::cerr << "Erreur de chargement" << std::endl; return;}


    while (std::getline(file, line) && r < rows) {
        std::istringstream ss(line);
        std::string cell;
        int c = 0;
        X[r].resize(columns);
        I[r].resize(columns);
        while (std::getline(ss, cell, ',') && c < columns) {
            double value = std::stod(cell);
            X[r][c] = value*c2;
            I[r][c] = value*c1;
            c++;
        }
        r++;
    }
}








void update(std::vector<std::vector<double> >& X, std::vector<std::vector<double> >& I) {
    //calcul Y en fonction de X
    for (int r = 0; r < rows; ++r) {
        for (int c = 0; c < columns; ++c) {
            Y[r][c]= 0.5*(abs(X[r][c]+1) - abs(X[r][c]-1));}}

    // convolution et stockage dans Y_convo
    for (int r = 0; r < rows; ++r) {
        for (int c = 0; c < columns; ++c) {
            sumY = 0;
            for (int i = -2; i <= 2; ++i) {
                for (int j = -2; j <= 2; ++j) {
                    int wrappedR = wrap(r + i, rows);
                    int wrappedC = wrap(c + j, columns);
                    sumY += X[wrappedR][wrappedC] * kernel5[i + 2][j + 2]; }}
            Y_convo[r][c]=sumY;    
            }
        }


    //calcul de X(t+1)
    for (int r = 0; r < rows; ++r) {
        for (int c = 0; c < columns; ++c) {
            X[r][c]+=Y_convo[r][c]+I[r][c];
        }
    }

}


// initialization grid
void setup(std::vector<std::vector<double> >& A, std::vector<std::vector<double> >& B) {
    loadCSV(A,B,"bin/data/grid.csv");
}




int main() {
    std::vector<std::vector<double> > X(rows, std::vector<double>(columns));
    std::vector<std::vector<double> > Y(rows, std::vector<double>(columns));
    std::vector<std::vector<double> > X0(rows, std::vector<double>(columns));
    std::vector<std::vector<double> > I(rows, std::vector<double>(columns));

    setup(X0, I);
    X=X0;

    //nombre updates
    for (int i = 0; i < 5; ++i) {
        update(X, I);
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
                pixel.setFillColor(sf::Color(std::min(255.0, X[r][c] * 255), std::min(255.0, (1-X[r][c]) * 255), 0));
                window.draw(pixel);
            }
        }

        window.display();
    }

    return 0;
}
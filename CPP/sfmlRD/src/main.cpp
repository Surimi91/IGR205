#include <SFML/Graphics.hpp>
#include <iostream>
#include <vector>
#include <random>
#include <fstream>
#include <sstream>
#include <string>



// constantes
const int c2=1;
const int c1=2;

int k;
int l;

double sumY;

const int rows = 512;
const int columns = 512;
const int pixelSize = 1;

const float S=0;  //S=0 donne le basic RD
const int steps=500;

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
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < columns; ++j) {
            sumY = 0;
            for (int u = -2; u <= 2; ++u) {
                for (int v = -2; v <= 2; ++v) {
                    k=i+u; l=j+v;
                    k=i+(u/(1-S));  l=j+(v/(1-S));
                    int wrappedK = wrap(k, rows);
                    int wrappedL = wrap(l, columns);
                    sumY += Y[wrappedK][wrappedL] * kernel5[u+2][v+2]; }}
            Y_convo[i][j]=sumY;   
            //Y_convo[i][j]=(1+sumY)/2;  //Accordingly, the output Y within the range [−1, 1] requires the inverse mapping f −1 (x) = (x + 1)/2
            }
        }


    //calcul de X(t+1)
    for (int r = 0; r < rows; ++r) {
        for (int c = 0; c < columns; ++c) {
            X[r][c]+=(Y_convo[r][c]+I[r][c]);
        }
    }

}


// initialization grid
void setup(std::vector<std::vector<double> >& A, std::vector<std::vector<double> >& B) {
    loadCSV(A,B,"bin/data/grid.csv");
}




void saveGridToCSV(const std::vector<std::vector<double> >& grid, const std::string& filename) {
    std::ofstream file(filename);
    if (!file.is_open()) {
        std::cerr << "pas ouvert.\n";
        return;
    }
    
    for (const auto& row : grid) {
        for (size_t i = 0; i < row.size(); ++i) {
            file << row[i];
            if (i < row.size() - 1) file << ",";
        }
        file << "\n";
    }
    file.close();
}





int main() {
    std::vector<std::vector<double> > X(rows, std::vector<double>(columns));
    std::vector<std::vector<double> > Y(rows, std::vector<double>(columns));
    std::vector<std::vector<double> > X0(rows, std::vector<double>(columns));
    std::vector<std::vector<double> > I(rows, std::vector<double>(columns));

    setup(X0, I);
    X=X0;

    //nombre updates
    for (int i = 0; i < steps; ++i) {
        update(X, I);
    }



    sf::RenderWindow window(sf::VideoMode(columns * pixelSize, rows * pixelSize), "Simulation Results");


    sf::Texture texture;
    texture.create(window.getSize().x, window.getSize().y);

    
     while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();

            // Ajout de la gestion de l'appui sur la touche A
            if (event.type == sf::Event::KeyPressed) {
                if (event.key.code == sf::Keyboard::A) {
                    window.close();
                }
            }
        }
     

        window.clear();

        for (int r = 0; r < rows; ++r) {
            for (int c = 0; c < columns; ++c) {
                sf::RectangleShape pixel(sf::Vector2f(pixelSize, pixelSize));
                pixel.setPosition(c * pixelSize, r * pixelSize);
                pixel.setFillColor(sf::Color(std::min(255.0, X[r][c] * 255), std::min(255.0, (1-X[r][c]) * 255), 0));
                pixel.setFillColor(sf::Color(std::min(255.0, (1-X[r][c]) * 255), std::min(255.0, (1-X[r][c]) * 255), std::min(255.0, (1-X[r][c]) * 255)));
                //pour le N et B
                window.draw(pixel);
            }
        }

        window.display();



                // Capture de la fenêtre
        texture.update(window);
        sf::Image screenshot = texture.copyToImage();


        for (int r = 0; r < rows; ++r) {
            for (int c = 0; c < columns; ++c) {
                if (X[r][c]>0.5){
                    X[r][c]=1;
                } else{X[r][c]=0;}
            }
        }
        // Enregistrement de l'image en PNG
        saveGridToCSV(X,"bin/data/output.csv");

        screenshot.saveToFile("screenshot.png");
    }

    return 0;
}
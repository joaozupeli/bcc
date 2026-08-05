import processing.sound.*;
import java.io.File;

PImage alfabeto;
String tela = "inicio";

// Nomes dos arquivos de som
String[] letras = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"};
SoundFile[] sons = new SoundFile[26];

// Coordenadas calculadas para a imagem 700x700
// Estrutura: [coluna, linha]
float margemX = 105; // Início da primeira letra (A)
float margemY = 110; // Topo da primeira linha
float passoX = 120;  // Distância horizontal entre centros
float passoY = 135;  // Distância vertical entre centros
float tamBotao = 90; // Tamanho da área de clique

void setup() {
  size(700, 700);
  alfabeto = loadImage("alfabeto.png");
 
  // Carregar sons
  for (int i = 0; i < 26; i++) {
    String path = dataPath(letras[i] + ".mp3");
    if (new File(path).exists()) {
      sons[i] = new SoundFile(this, letras[i] + ".mp3");
    } else {
      println("Aviso: " + letras[i] + ".mp3 não encontrado.");
    }
  }
}

void draw() {
  background(255);
 
  if (tela.equals("inicio")) {
    desenhaInicio();
  } else if (tela.equals("alfabeto")) {
    desenhaAlfabeto();
  }
}

void desenhaInicio() {
  textAlign(CENTER, CENTER);
  fill(50, 50, 200);
  textSize(50);
  text("MONSTER ABC", width/2, height/3);
 
  // Botão Jogar
  fill(100, 200, 100);
  rect(width/2 - 100, 450, 200, 60, 20);
  fill(255);
  textSize(25);
  text("COMEÇAR", width/2, 480);
}

void desenhaAlfabeto() {
  image(alfabeto, 0, 0, width, height);
 
  // Botão Voltar
  fill(255, 100, 100);
  rect(10, 10, 80, 35, 10);
  fill(255);
  textSize(15);
  text("VOLTAR", 50, 27);
 
  /* DESCOMENTE A LINHA ABAIXO PARA VER OS QUADRADOS DE CLIQUE
     E TER CERTEZA QUE ESTÃO NO LUGAR CERTO
  */
  // mostrarGrades();
}

void mousePressed() {
  if (tela.equals("inicio")) {
    if (mouseX > width/2 - 100 && mouseX < width/2 + 100 && mouseY > 450 && mouseY < 510) {
      tela = "alfabeto";
    }
  }
  else if (tela.equals("alfabeto")) {
    if (mouseX > 10 && mouseX < 90 && mouseY > 10 && mouseY < 45) {
      tela = "inicio";
    } else {
      verificarCliqueLetra();
    }
  }
}

void verificarCliqueLetra() {
  for (int i = 0; i < 26; i++) {
    // Cálculo da posição de cada letra baseado na imagem enviada
    int col = i % 5;
    int lin = i / 5;
   
    // Ajuste especial para a última linha (W, X, Y, Z) que tem 4 letras e é centralizada
    float x, y;
    if (lin < 4) {
      x = margemX + (col * passoX);
      y = margemY + (lin * passoY);
    } else {
      // A última linha começa um pouco mais para a direita para centralizar
      x = margemX + 55 + ((i - 20) * passoX);
      y = margemY + (lin * passoY);
    }
   
    // Se o mouse estiver dentro do quadrado da letra
    if (mouseX > x - tamBotao/2 && mouseX < x + tamBotao/2 &&
        mouseY > y - tamBotao/2 && mouseY < y + tamBotao/2) {
     
      if (sons[i] != null) {
        sons[i].stop();
        sons[i].play();
      }
      println("Letra: " + letras[i].toUpperCase());
      break;
    }
  }
}

// Função auxiliar apenas para teste visual
void mostrarGrades() {
  noFill();
  stroke(255, 0, 0, 150);
  for (int i = 0; i < 26; i++) {
    int col = i % 5;
    int lin = i / 5;
    float x, y;
    if (lin < 4) {
      x = margemX + (col * passoX);
      y = margemY + (lin * passoY);
    } else {
      x = margemX + 55 + ((i - 20) * passoX);
      y = margemY + (lin * passoY);
    }
    rect(x - tamBotao/2, y - tamBotao/2, tamBotao, tamBotao);
  }
}
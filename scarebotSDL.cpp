#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_mixer.h>
#include <SDL2/SDL_ttf.h>
#include <stdio.h>
#include <stdbool.h> //bool
#include <cstdlib> //random
#include <math.h> //ceil()
#include <string>


int width = 320, height = 240;
SDL_Window *win = NULL;
win = SDL_CreateWindow("Hello World", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, width, height, 0);
int jspeeed = -16;
float speeed = 4.5*2;
int plus_un = 0; //variable pour régler les nuages à leur bon emplacement

class Sol
{
	private:
		int x;
		int y;
		int type;
		sf::Texture t_sol1;
		sf::Sprite s_sol1;
		sf::Texture t_sol2;
		sf::Sprite s_sol2;
		sf::Texture t_sol3;
		sf::Sprite s_sol3;
	public:
		Sol()
		{
			x = 0;
			y = 203;
			type = std::rand()/((RAND_MAX + 1u)/3);
			t_sol1.loadFromFile("images/sol 1.png");
			s_sol1.setTexture(t_sol1);

			t_sol2.loadFromFile("images/sol 2.png");
			s_sol2.setTexture(t_sol2);
			
			t_sol3.loadFromFile("images/sol 3.png");
			s_sol3.setTexture(t_sol3);
		}
		void Reset()
		{
			type = std::rand()/((RAND_MAX + 1u)/3);
		}
		void setX(int xx) {x = xx;}
		int getX() {return x;}
		void draw()
		{
			if(type == 0){s_sol1.setPosition(x, y); window.draw(s_sol1);}
			else if(type == 1){s_sol2.setPosition(x, y); window.draw(s_sol2);}
			else if (type==2){s_sol3.setPosition(x, y); window.draw(s_sol3);}
		}
		void update()
		{
			x = x-(int)speeed;
			if(x<=-33)
			{
				x = 330 + (33+x);
				type = std::rand()/((RAND_MAX + 1u)/3); //random 0 1 ou 2
			}
			switch(type) 
			{
				case 0:
					s_sol1.setPosition(x, y); 
					window.draw(s_sol1);
		  			break;
				case 1:
					s_sol2.setPosition(x, y); 
					window.draw(s_sol2);
					break;
				default: //case 2
					s_sol3.setPosition(x, y); 
					window.draw(s_sol3);
			}
		}
};

int main() 
{
	TTF_Init();
	if( SDL_Init( SDL_INIT_VIDEO | SDL_INIT_AUDIO ) < 0 )
	{
		printf( "SDL could not initialize! SDL Error: %s\n", SDL_GetError() );
	}
        if( Mix_OpenAudio( 44100, MIX_DEFAULT_FORMAT, 2, 2048 ) < 0 )
        {
            printf( "SDL_mixer could not initialize! SDL_mixer Error: %s\n", Mix_GetError() );
        }
	int score=0;

	SDL_Renderer *renderer = NULL;
	SDL_Texture *blobTex = NULL;
	SDL_Surface *blobSurface = NULL;

	//The music that will be played
	Mix_Music *gMusic = NULL;
 	
	//The sound effects that will be used
	Mix_Chunk *gScratch = NULL;
	const char *cstr;

	TTF_Font * font = TTF_OpenFont("./images/pixelmix_bold.ttf", 12);
	SDL_Color color = { 48, 98, 48 };
	

	SDL_Rect SrcR, SrcScore;
	SDL_Rect DestR, DestScore;
	float fps=30.0;
// à l'intérieur du render :
	SrcR.x = 0;
	SrcR.y = 0;
	SrcR.w = 58;
	SrcR.h = 31;

	DestR.x = 10;
	DestR.y = 180;
	DestR.w = 58;
	DestR.h = 31;

	SrcScore.x = 0;
	SrcScore.y = 0;
	SrcScore.w = 125;
	SrcScore.h = 11;

	DestScore.x = 200;
	DestScore.y = 10;
	DestScore.w = 90;
	DestScore.h = 11;

	std::string s_score;

	gScratch = Mix_LoadWAV( "./Musiques/sfxScarebotGameOver.wav" );
	gMusic = Mix_LoadMUS( "./Musiques/8bit.wav" );

	renderer = SDL_CreateRenderer(win, -1, SDL_RENDERER_ACCELERATED);

	SDL_Surface * scoreSurf = TTF_RenderText_Solid(font, "Score: 5", color);
	SDL_Texture * scoreTex = SDL_CreateTextureFromSurface(renderer, scoreSurf);
	SDL_FreeSurface(scoreSurf);

	blobSurface = IMG_Load("./images/blob_base.png");
	blobTex = SDL_CreateTextureFromSurface(renderer, blobSurface);
	SDL_FreeSurface(blobSurface);

 	Mix_PlayMusic( gMusic, -1 ); // Musique en boucle
	Mix_PlayChannel( -1, gScratch, 0 );
	unsigned int a = SDL_GetTicks();
	unsigned int b = SDL_GetTicks();
	double delta = 0;
	while (1) 
	{
		SDL_Event e;
		if (SDL_PollEvent(&e)) 
		{
			if (e.type == SDL_QUIT) 
			{
				break;
			}
		}
		a = SDL_GetTicks();
		delta = a - b;

		if (delta > 1000/fps)
		{
			b = a;    

			score=score+1;
			s_score = "Score: "+std::to_string(score);
			cstr = s_score.c_str();
			scoreSurf = TTF_RenderText_Solid(font,cstr , color);
			scoreTex = SDL_CreateTextureFromSurface(renderer, scoreSurf);
			SDL_FreeSurface(scoreSurf);

			


			// Select the color for drawing. It is set to red here.
			SDL_SetRenderDrawColor(renderer, 172, 181, 107, 255); //coloriage du background

			// Clear the entire screen to our selected color.
			SDL_RenderClear(renderer);
			SDL_RenderCopy(renderer, scoreTex, &SrcScore, &DestScore);
			SDL_RenderCopy(renderer, blobTex, &SrcR, &DestR);
			SDL_RenderPresent(renderer);
		}


	}
	//Free the sound effects
	Mix_FreeChunk( gScratch );
	gScratch = NULL;
	//Free the music
	Mix_FreeMusic( gMusic );
	gMusic = NULL;
	TTF_CloseFont(font);
	SDL_DestroyTexture(scoreTex);
	SDL_DestroyTexture(blobTex);
	SDL_DestroyRenderer(renderer);
	SDL_DestroyWindow(win);
	TTF_Quit();
	Mix_Quit();
	IMG_Quit();
	SDL_Quit();
	

	return 0;
}
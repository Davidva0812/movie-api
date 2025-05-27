import requests
import pygame
import sys
from io import BytesIO
from config import my_key

API_KEY = my_key
URL = "https://www.omdbapi.com"


def get_movie_data(title_input):
    payload = {"t": title_input, "apikey": API_KEY}
    movie_response = requests.get(URL, payload)
    data = movie_response.json()
    poster_url = data.get("Poster")
    poster_img = None

    # Handling status codes
    if movie_response.status_code == 200:
        title = data["Title"]
        date = data["Year"]
        rating = data["imdbRating"]
        director = data["Director"]
        actors = data["Actors"]
        if poster_url and poster_url != "N/A":
            try:
                response = requests.get(poster_url)
                image_file = BytesIO(response.content)
                poster_img = pygame.image.load(image_file)
                poster_img = pygame.transform.smoothscale(poster_img, (250, 350))
            except Exception as e:
                print("Poster loading error:", e)

        return title, date, rating, director, actors, poster_img

    if movie_response.status_code == 401:
        print("401: Unauthorized: Wrong API key!")
    elif movie_response.status_code == 404:
        print("404: Not Found: Wrong data!")
    elif movie_response.status_code == 429:
        print("429: Too many requests!")
    else:
        # For other errors, provide a generic message
        print(f"Error: {data['message']}!")
    return None


# Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Movie App")
font = pygame.font.SysFont(None, 32)
clock = pygame.time.Clock()

input_box = pygame.Rect(50, 10, 300, 40)
set_mode_button = pygame.Rect(370, 10, 100, 40)
color_inactive = pygame.Color('gray')
color_active = pygame.Color((69, 71, 74))
color = color_inactive
active = False
text = ""
mode = "Light"
movie_data = None
poster_img = None


def draw_text(surface, text, pos, font, color):
    surface.blit(font.render(text, True, color), pos)


# Main loop
while True:
    # Set text color based on mode
    text_color = (0, 0, 0) if mode == "Light" else (161, 160, 153)
    if mode == "Light":
        screen.fill((145, 102, 1))
    else:
        screen.fill((40, 40, 60))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
            if set_mode_button.collidepoint(event.pos):
                mode = "Dark" if mode == "Light" else "Light"

        # Check if a key is pressed and the input field is active
        if event.type == pygame.KEYDOWN and active:
            # If the user presses Enter (Return key):
                # Capitalize the city name from the typed text
                # Get data for the entered movie
            if event.key == pygame.K_RETURN:
                title_input = text.strip().capitalize()
                result = get_movie_data(title_input)
                # If the movie data is successfully fetched
                if result:
                    title, date, rating, director, actors, poster_img  = result
                    movie_data = {
                        "Title": title,
                        "Year": date,
                        "IMDB Rating": rating,
                        "Director": director,
                        "Actors": actors,
                        "Poster": poster_img
                    }
                # Clear the input text after Enter is pressed
                text = ""
            # If the user presses Backspace, remove the last character from text
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            # Otherwise, add the typed character to the text
            else:
                text += event.unicode

        # Input field
        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface = font.render(text, True, (212, 210, 210))
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        # Mode changing button
        pygame.draw.rect(screen, (135, 134, 128) if mode == "Light" else  (70, 70, 90), set_mode_button)
        draw_text(screen, "Dark" if mode == "Light" else "Light",
                  (set_mode_button.x + 30, set_mode_button.y + 10), font,
                  (255, 255, 255) if mode == "Light" else (0, 0, 0))


        if movie_data:
            draw_text(screen, f"Title: {movie_data['Title']}",
                      (50, 90), font, text_color)
            draw_text(screen, f"Year: {movie_data['Year']}",
                      (50, 120), font, text_color)
            draw_text(screen, f"IMDB Rating: {movie_data['IMDB Rating']}",
                      (50, 150), font, text_color)
            draw_text(screen, f"Director: {movie_data['Director']}",
                      (50, 180), font, text_color)
            draw_text(screen,
                      f"Actors: {movie_data['Actors']}",
                      (50, 210), font, text_color)
            screen.blit(poster_img, (270, 245))

        pygame.display.flip()
        clock.tick(30)
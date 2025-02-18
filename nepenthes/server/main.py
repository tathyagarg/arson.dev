import random
import socket
import time
import threading
import argparse
import collections
import string

parser = argparse.ArgumentParser(description="Simple HTTP server")
parser.add_argument("--port", type=int, default=8080, help="Port to run the server on")
parser.add_argument("--max-backlog", type=int, default=5, help="Maximum number of pending connections")
parser.add_argument("--host", type=str, default="", help="Host to run the server on")
parser.add_argument("--template", type=str, default="data/template.html", help="Template to render")
parser.add_argument("--sentence-count", type=int, default=3, help="Number of sentences to generate")
parser.add_argument("--link-count", type=int, default=5, help="Number of links to generate")

parser.add_argument("--filename", type=str, default="data/shakespeare.txt", help="File to read data from")
parser.add_argument("--n", type=int, default=3, help="N-gram size")
parser.add_argument("--threshold", type=int, default=20, help="Threshold for sentence generation")

class Babbler:
    def __init__(self, filename: str, n: int = 3, threshold: int = 20) -> None:
        self.filename = filename
        self.starters = []
        self.stoppers = []

        self.dictionary = collections.defaultdict(list)
        self.n = n
        self.threshold = threshold 

        self.add_file()

    def add_sentence(self, sentence: str) -> None:
        words = sentence.split()
        words = [word.strip(string.punctuation).replace('\'', '') for word in words]

        ngram = " ".join(words[:self.n])

        self.starters.append(ngram)
        self.stoppers.append(" ".join(words[-self.n:]))

        for word in words[self.n:]:
            self.dictionary[ngram].append(word)
            ngram = " ".join(ngram.split()[1:] + [word])

    def add_file(self) -> None:
        with open(self.filename) as f:
            for line in f.readlines():
                if line := line.strip():
                    self.add_sentence(line.lower())


    def babble(self, start: str = "") -> str:
        ngram = start or random.choice(self.starters)
        sentence = ngram.split()

        count = self.n
        while ngram not in self.stoppers or count < self.threshold:
            try:
                next_word = random.choice(self.dictionary[ngram])
                sentence.append(next_word)

                ngram = " ".join(sentence[-self.n:])
                count += 1
            except IndexError:
                break

        return " ".join(sentence)

    def random_starter(self) -> str:
        return random.choice(self.starters)

class Server:
    def __init__(
        self,
        babbler: Babbler,
        port: int = 8080,
        max_backlog: int = 5,
        host: str = "",
        template: str = "data/template.html",
        sentence_count: int = 3,
        link_count: int = 5,
    ) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(max_backlog)

        self.babbler = babbler
        self.sentence_count = sentence_count
        self.link_count = link_count

        with open(template) as f:
            self.template = f.read()

    def run(self) -> None:
        while True:
            client, _ = self.server.accept()
            request_data: str = client.recv(1024).decode()

            threading.Thread(
                target=self.handle_client, args=(request_data, client),
                daemon=True
            ).start()

    def get_endpoint(self, data: str) -> str:
        return data.split(" ")[1]

    def handle_client(self, request_data: str, client) -> None:
        response = self.handle_request(request_data)
        for i in range(0, len(response), 10):
            client.send(response[i:i+10].encode())
            time.sleep(0.5)

        client.close()


    def handle_request(self, data: str) -> str:
        endpoint = self.get_endpoint(data)

        h1 = self.babbler.random_starter() if endpoint == "/" else endpoint[1:]
        p = self.babbler.babble(h1)
        for i in range(self.sentence_count):
            p += ". " + self.babbler.babble()
        p += "."

        lis = [self.babbler.random_starter() for _ in range(self.link_count)]
        lis = [f"<li><a href=\"/{li}\">{li}</a></li>" for li in lis]

        return "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + self.template.format(h1=h1, p=p, lis='\n'.join(lis))

def main():
    args = parser.parse_args()
    babbler = Babbler(filename=args.filename, n=args.n, threshold=args.threshold)

    server = Server(babbler, port=args.port, max_backlog=args.max_backlog, host=args.host, sentence_count=args.sentence_count, link_count=args.link_count,)
    server.run()

if __name__ == "__main__":
    main()


import json
import os
import argparse

FILE_PATH = 'notes.json'
STATUSES = ['pendiente', 'resuelto', 'listo', 'cerrado']

class NoteSystem:
    def __init__(self, path=FILE_PATH):
        self.path = path
        self.notes = self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.notes, f, indent=2, ensure_ascii=False)

    def add(self, text, status='pendiente', shared_with=None):
        if status not in STATUSES:
            raise ValueError(f"Estado invalido: {status}")
        note_id = 1 if not self.notes else self.notes[-1]['id'] + 1
        self.notes.append({
            'id': note_id,
            'text': text,
            'status': status,
            'shared_with': shared_with or []
        })
        self.save()
        print(f'Nota creada con id {note_id}')

    def list(self):
        if not self.notes:
            print('No hay notas.')
            return
        for note in self.notes:
            shared = ', '.join(note.get('shared_with', [])) or '-'
            print(f"{note['id']}: {note['text']} [{note['status']}] compartido con: {shared}")

    def set_status(self, note_id, status):
        if status not in STATUSES:
            raise ValueError(f"Estado invalido: {status}")
        for note in self.notes:
            if note['id'] == note_id:
                note['status'] = status
                self.save()
                print(f'Nota {note_id} actualizada a {status}')
                return
        print('Nota no encontrada.')

    def share(self, note_id, users):
        for note in self.notes:
            if note['id'] == note_id:
                existing = set(note.get('shared_with', []))
                existing.update(users)
                note['shared_with'] = list(existing)
                self.save()
                print(f'Nota {note_id} compartida con: {", ".join(users)}')
                return
        print('Nota no encontrada.')

def parse_users(value):
    return [u.strip() for u in value.split(',') if u.strip()]

def main():
    parser = argparse.ArgumentParser(description='Sistema simple de notas')
    subparsers = parser.add_subparsers(dest='command')

    p_add = subparsers.add_parser('add', help='Crear una nota')
    p_add.add_argument('text', help='Texto de la nota')
    p_add.add_argument('--status', default='pendiente', choices=STATUSES, help='Estado inicial')
    p_add.add_argument('--shared', default='', help='Usuarios separados por coma')

    subparsers.add_parser('list', help='Listar notas')

    p_status = subparsers.add_parser('status', help='Cambiar estado de una nota')
    p_status.add_argument('id', type=int, help='ID de la nota')
    p_status.add_argument('status', choices=STATUSES, help='Nuevo estado')

    p_share = subparsers.add_parser('share', help='Compartir una nota con usuarios')
    p_share.add_argument('id', type=int, help='ID de la nota')
    p_share.add_argument('users', help='Usuarios separados por coma')

    args = parser.parse_args()
    system = NoteSystem()

    if args.command == 'add':
        users = parse_users(args.shared)
        system.add(args.text, status=args.status, shared_with=users)
    elif args.command == 'list':
        system.list()
    elif args.command == 'status':
        system.set_status(args.id, args.status)
    elif args.command == 'share':
        users = parse_users(args.users)
        system.share(args.id, users)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

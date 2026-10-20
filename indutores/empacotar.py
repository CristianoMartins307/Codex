#!/usr/bin/env python3
"""Cria o pacote portátil dos arquivos gerados. Não inclui PDFs de referência."""
from pathlib import Path
import hashlib
import zipfile


def main():
    root = Path(__file__).resolve().parent
    names = [
        'README.md', 'GUIA_PROJETO.md', 'EXEMPLO_RESOLVIDO.md', 'PROJETO.md',
        'LEIA_AQUI_Guia_e_Projeto.md', 'LEIA_AQUI_Guia_e_Projeto.txt',
        'CODIGO_Analise_Correntes.txt', 'CODIGO_Exemplo_Resolvido.txt',
        'calculo.py', 'exemplo_completo.py', 'parametros_exemplo.json',
        'parametros_projeto_exemplo.json', 'gerar_figuras.py',
        'escrever_exemplo.py', 'gerar_pdfs.py', 'cabecalho_pdf.tex',
        'requirements.txt', 'empacotar.py',
    ]
    files = [root / name for name in names]
    for folder in ['pdf', 'dados', 'resultados', 'resultados_exemplo',
                   'figuras', 'verificacao', 'historico']:
        files.extend(f for f in sorted((root / folder).rglob('*')) if f.is_file())
    for f in files:
        if not f.is_file():
            raise FileNotFoundError(f)
        if f.is_symlink() or not f.resolve().is_relative_to(root):
            raise ValueError(f'Caminho não permitido: {f}')
    manifest = root / 'MANIFESTO_SHA256.txt'
    manifest.write_text(''.join(
        hashlib.sha256(f.read_bytes()).hexdigest() + '  ' +
        f.relative_to(root).as_posix() + '\n' for f in files
    ), encoding='utf-8')
    files.append(manifest)
    output = root / 'pacotes'
    output.mkdir(exist_ok=True)
    archive = output / 'Projeto_Indutores_Pacote_Completo.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for f in files:
            z.write(f, 'Projeto_Indutores/' + f.relative_to(root).as_posix())
    with zipfile.ZipFile(archive) as z:
        bad = z.testzip()
        if bad is not None:
            raise RuntimeError(f'Falha de integridade: {bad}')
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / (archive.name + '.sha256')).write_text(
        digest + '  ' + archive.name + '\n', encoding='utf-8')
    print(f'{archive.name}: {len(files)} arquivos; {archive.stat().st_size} bytes')
    print('SHA-256:', digest)


if __name__ == '__main__':
    main()

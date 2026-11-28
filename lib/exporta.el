;;; exporta.el --- exportar en batch el org de un vídeo a html  -*- lexical-binding: t -*-
;;
;; Uso, desde la raíz del repositorio:
;;   emacs --batch -l lib/exporta.el --visit=L01-VYY-Nombre.org -f org-html-export-to-html
;;
;; Carga htmlize (para colorear el código, como en V05-V09) y no evalúa ningún bloque al
;; exportar: ni `#+call: guion(...)` ni `montaje` deben ejecutarse.
;;
;; Aspecto común de las webs de Álgebra Lineal (2026-11-27; reglas en
;; ../coordinacion/coordinacion-entre-repositorios.md): toda página sale con la hoja única
;; (sin el estilo por defecto de Org) y con la barra de enlaces justo detrás del título.
;; Las páginas de los vídeos llevan la barra por decisión de Marcos (2026-11-28), aunque la
;; regla general la reserva a las portadas: así se vuelve de ellas a la portada y a las otras
;; webs. Si la barra cambia, cambiarla aquí, en index.org y en los html ya publicados.
;; La portada (index.org) trae su propia barra y también se exporta así:
;;   emacs --batch -l lib/exporta.el --visit=index.org -f org-html-export-to-html

(dolist (d (file-expand-wildcards "~/.emacs.d/elpa/htmlize-*"))
  (add-to-list 'load-path d))
(require 'htmlize)
(require 'org)
(setq org-confirm-babel-evaluate nil
      org-export-use-babel nil)

(require 'ox-html)
(setq org-html-head-include-default-style nil
      org-html-head
      "<link rel=\"stylesheet\" href=\"https://mbujosab.github.io/css/algebra-lineal.css\">")

(defconst vm2-barra-comun
  "<nav class=\"blocknav\" aria-label=\"Webs de Álgebra Lineal\">
  <div class=\"container\">
    <a href=\"https://mbujosab.github.io/CursoDeAlgebraLineal/\">Libro</a>
    <a href=\"https://mbujosab.github.io/MatematicasII/\">Material de clase</a>
    <a href=\"https://mbujosab.github.io/nacal-Jupyter-Notebooks/\">Notebooks</a>
    <a href=\"https://mbujosab.github.io/VideosMates2/\" aria-current=\"page\">Vídeos</a>
    <a href=\"https://mbujosab.github.io/nacallib/\">NAcAL</a>
    <a href=\"https://mbujosab.github.io/nacal-latex-package/\">Paquete de LaTeX</a>
    <a href=\"https://mbujosab.github.io/\">Marcos Bujosa</a>
  </div>
</nav>
"
  "Barra común de las webs de Álgebra Lineal (HTML exacto de las reglas de coordinación).")

(defun vm2-pon-barra-comun (salida backend _info)
  "Inserta la barra común tras el título, salvo que el documento ya la traiga."
  (if (and (org-export-derived-backend-p backend 'html)
           (not (string-match-p "class=\"blocknav\"" salida))
           (string-match "<h1 class=\"title\">\\(?:.\\|\n\\)*?</h1>\n?" salida))
      (concat (substring salida 0 (match-end 0)) vm2-barra-comun (substring salida (match-end 0)))
    salida))
(add-to-list 'org-export-filter-final-output-functions #'vm2-pon-barra-comun)

;;; exporta.el ends here

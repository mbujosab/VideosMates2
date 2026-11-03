;;; exporta.el --- exportar en batch el org de un vídeo a html  -*- lexical-binding: t -*-
;;
;; Uso, desde la raíz del repositorio:
;;   emacs --batch -l lib/exporta.el --visit=L01-VYY-Nombre.org -f org-html-export-to-html
;;
;; Carga htmlize (para colorear el código, como en V05-V09) y no evalúa ningún bloque al
;; exportar: ni `#+call: guion(...)` ni `montaje` deben ejecutarse.
;; El index.html NO se exporta así (véase CLAUDE.md): su tema solo sale con C-c C-e h h
;; desde el Emacs de Marcos.

(dolist (d (file-expand-wildcards "~/.emacs.d/elpa/htmlize-*"))
  (add-to-list 'load-path d))
(require 'htmlize)
(require 'org)
(setq org-confirm-babel-evaluate nil
      org-export-use-babel nil)

;;; exporta.el ends here

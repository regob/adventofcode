;;; aoc-utils.el --- Utilities for AOC -*- lexical-binding: t -*-
;;; Commentary:
;;; Code:

(defvar aoc-utils-year 2024)

(defun aoc-load-input (day)
  "Load daily input into a list of strings."
  (let ((input-path (expand-file-name
                     (concat (format "%d" aoc-utils-year)
                             "_"
                             (format "%02d" day)
                             ".txt")
                     "../../input")))
    (with-temp-buffer
      (insert-file-contents input-path)
      (split-string (buffer-string) "\n" t))))

(provide 'aoc-utils)

;;; aoc-utils.el ends here

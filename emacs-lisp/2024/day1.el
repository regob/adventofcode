;;; day1.el --- summary -*- lexical-binding: t -*-
;;; Commentary:
;;; Code:

(add-to-list 'load-path default-directory)
(require 'cl-lib)
(require 'aoc-utils)

(defun parse-line (line)
  (mapcar 'string-to-number (split-string line " +" t)))

;; Part 1

(defun extract-sorted-nth (list n)
  (sort (mapcar (lambda (row) (nth n row))
                list
                )
        '<))

(defun total-sum-differences (list1 list2)
  (seq-reduce '+
              (cl-mapcar
               (lambda (x1 x2) (abs (- x1 x2)))
               list1
               list2)
              0
              ))


(defvar input-tuples (mapcar 'parse-line (aoc-load-input 1)))
(message "Part 1: %s" (total-sum-differences
                       (extract-sorted-nth input-tuples 0)
                       (extract-sorted-nth input-tuples 1)))

;; Part 2

(defun count-occurrences (lst)
  "Return an associative list with the count of each item in LST."
  (let (alist)
    (dolist (item lst)
      (let ((entry (assoc item alist)))
        (if entry
            (setcdr entry (1+ (cdr entry))) ;; Increment count if found
          (push (cons item 1) alist))))     ;; Otherwise, add new entry
    alist))


(defun total-similarity-score (list1 list2)
  "Total score of elements from LIST1 times their number of occurrence in LIST2."
  (let ((list2-counts (count-occurrences list2)))
    (seq-reduce '+
                (mapcar
                 (lambda (x) (* x (alist-get x list2-counts 0)))
                 list1)
                0)))

(message "Part 2: %s" (total-similarity-score (extract-sorted-nth input-tuples 0)
                                              (extract-sorted-nth input-tuples 1)))

(provide 'day1)

;;; day1.el ends here

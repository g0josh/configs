syntax on
set backspace=2
filetype plugin indent on
set encoding=utf-8
set number relativenumber
set cursorline
set t_Co=256
set clipboard=unnamedplus
set ruler

set foldmethod=manual

"Tabs and spacing
set autoindent
set cindent
set tabstop=4
set expandtab
set shiftwidth=4
set smarttab
nnoremap tn :tabnew<Space>
nnoremap tk :tabnext<CR>
nnoremap tj :tabprev<CR>
nnoremap th :tabfirst<CR>
nnoremap tl :tablast<CR>

"Search
set hlsearch
set incsearch
set ignorecase
set smartcase
set diffopt +=iwhite

" easy split movement
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l


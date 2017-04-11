thing Range
    has number end
    has number current

    setup with start, end
        self.current = start - 1
        self.end = end

    does next
        if self.current < self.end
            self.current = self.current + 1
            return self.current

    does has_next
        return self.current < self.end
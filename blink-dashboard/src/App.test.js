import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Blink Tracker heading', () => {
  render(<App />);
  expect(screen.getByText(/Blink Tracker/i)).toBeInTheDocument();
});
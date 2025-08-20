import { render, screen } from '@testing-library/react';
import App from '../src/App';

test('renders login form', () => {
  render(<App />);
  expect(screen.getByText(/login/i)).toBeInTheDocument();
});
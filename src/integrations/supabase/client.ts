import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://tzybtsfchkenoojmvfdc.supabase.co';
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ极XBhYmFzZSIsInJlZiI6InR6eWJ0c2ZjaGtlbm9vam12ZmRjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg5ODY2NzQsImV4cCI6MjA3NDU2MjY3NH0.JBJw60vcOMpoNmIg5lokX8rbgbMkDsLc_bM-7kNeWfg';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);